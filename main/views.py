import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import status, renderers
from accounts.models import Users
from config.utils.login_required import login_check
from .models import Post, user_reservation, Road, Level
from .serializer import Post_check, user_reservation_check, search, Account_check
from django.core.paginator import Paginator #페이지
from datetime import datetime
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

def pk_check(pk, num):
    if num == 1:
        post = Post.objects.get(id=pk)
        if post.remove == False and post.clear == False and post.Done == False:
            return False
    elif num == 2:
        post = user_reservation.objects.get(id=pk)
        if post.remove == False:
            return False
def road_check(road_user, road):
    try:
        check = Road.objects.get(user=road_user, road_check=False)
    except Road.DoesNotExist:
        check = Road.objects.create(user=road_user)
        check.road+=">{}".format(road)
        check.road_num += 1
        check.save()
    else:
        check.road += ">{}".format(road)
        check.road_num += 1
        if check.road_num >= 10 or road == "로그아웃":
            check.road_check = True
            check.save()
        check.save()

class Post_make(LoginRequiredMixin, APIView): # 예약 게시판 만들기
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        if request.user.nickname == '':
            return redirect('main:Main_check')
        day = datetime.now()
        min_day = str(day.date())
        return Response(status=status.HTTP_200_OK, template_name='main/write.html', data={'min_day': min_day})

    def post(self, request):
        form = Post_check(data=request.data, context={'request': request})
        day = datetime.now()
        min_day = str(day.date())
        if form.is_valid():
            form.save(car_user=request.user, context={'request': request})
            # obj = Post.objects.filter(car_user=request.user).order_by('-id')[0]
            # obj.users.add(request.user)
            road_check(request.user, "예약 게시판 생성")
            return redirect('main:list')
        else:
            error = str(form.errors)
            return Response(status=status.HTTP_200_OK, template_name='main/write.html', data={'form': form, 'min_day': min_day, 'error' : error})

class Post_list(LoginRequiredMixin, APIView): # 예약 게시글 리스트 @수정 완
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        if request.user.nickname == '':
            return redirect('main:Main_check')
        post_check = Post.objects.filter(clear=False, remove=False, Done=False)

        seoul_check = Post.objects.filter(clear=False, remove=False, Done=False, end_region='서울')
        gye_check = Post.objects.filter(clear=False, remove=False, Done=False, end_region='경기')
        inch_check = Post.objects.filter(clear=False, remove=False, Done=False, end_region='인천')
        remain_check = Post.objects.filter(~Q(end_region='서울'), ~Q(end_region="인천"), ~Q(end_region="경기"), clear=False, remove=False, Done=False)
        post_form = post_check.order_by('-create_date')
        seoul_form = seoul_check.order_by('-create_date') # 서울 @수정 완
        inch_form = inch_check.order_by('-create_date') # 인천 @수정 완
        gye_form = gye_check.order_by('-create_date') # 경기 @수정 완
        remain_form = remain_check.order_by('-create_date') # 그 외 @수정 완
        car = Users.objects.get(nickname=request.user)
        user = request.user
        road_check(request.user, "예약 게시판")
        return Response(status=status.HTTP_200_OK, template_name='main/trash/noticeboard.html',
                        data={'board_lists': post_form, 'seoul_lists': seoul_form, 'inch_lists': inch_form,'gye_lists': gye_form
                            ,'remain_lists': remain_form, 'car': car, 'user': user})
                            # car=게시글 유저 닉네임, user = 현재 로그인 되어 있는 닉네임

class Select_Post(LoginRequiredMixin, APIView): #선택한 예약 게시글
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk):
        if request.user.nickname == '':
            return redirect('main:Main_check')
        check = pk_check(pk, 1)
        if check == False:
            post = Post.objects.get(id=pk)
            user = request.user
            users = len(post.users.all()) - 1
            road_check(request.user, "{}번째 예약 게시판".format(pk))
            return Response(status=status.HTTP_200_OK,
                            template_name='main/post_iframe.html',
                            data={'post': post, 'pk': pk, 'users': users, 'user': user})
        else:
            return redirect('main:list')

    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        user_Count = len((post.users.all()))
        if user_Count < post.user_limit:
            post.users.add(request.user)
            post.num = user_Count
            post.save()
            road_check(request.user, "{}번째 예약 게시판의 유저예약".format(pk))
            return redirect('main:posts', pk)
        elif user_Count == len((post.users.all())):
            post.Done = True
            post.save()
            return Response(status=status.HTTP_200_OK,
                            template_name='main/post.html',
                            data={'post': post, 'pk': pk})
        else:
            post.Done = True
            post.save()
            return Response(status=status.HTTP_200_OK,
                        template_name='main/post.html',
                        data={'post': post, 'pk': pk})

class Reservation_searched(LoginRequiredMixin, APIView): #예약 게시글 찾기
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        if request.user.nickname == '':
            return redirect('main:Main_check')
        form = search(data=request.data)
        return Response(status=status.HTTP_200_OK,
                        template_name='main/reservation_write.html',
                        data={'form': form})

    def post(self, request):
        form = search(data=request.data)
        if form.is_valid():
            date = form['reservation_date'].value
            max_money, min_money = form['max_money'].value, form['min_money'].value
            max_time, min_time = form['max_time'].value, form['min_time'].value
            post = Post.objects.filter(date=date, time__range=[min_time, max_time], money__range=[min_money, max_money])
            road_check(request.user, "예약 게시글 찾기")
            return Response(status=status.HTTP_200_OK,
                        template_name='main/search.html',
                        data={'board_list': post})
        else:
            return Response(status=status.HTTP_200_OK,
                            template_name='main/reservation_write.html',
                            data={'form': form})
class My_page(LoginRequiredMixin, APIView): # 마이 페이지
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        if request.user.nickname == '':
            return redirect('main:Main_check')
        user = Users.objects.get(nickname=request.user)
        post = Post.objects.filter(car_user=request.user, clear=False, remove=False, Done=False)
        user_post = user_reservation.objects.filter(remove=False, user=request.user)
        my_post = post.order_by('-create_date')
        my_user_post = user_post.order_by('-create_date')

        # if Post.objects.all() == None:
        #     pass
        # else:
        #     for i in my_post:
        #         str_date = str(i.date)[6:10]
        #         str_time = str(i.time)[:5]
        #
        #     str_date = re.split(r'-', str_date)
        #     str_time = re.split(r':', str_time)
        #     result = list(str_date + str_time)
        #     date_values = []
        #     strings = ['now', 'month', 'day', 'hour', 'minute']
        #     for string in strings:
        #         value = getattr(timezone.now(), string)
        #         date_values.append(value)
        #     date_values.pop(0)
        #     date_values = str(date_values)
        #     print(result)
        #     print(date_values)



        road_check(request.user, "내 페이지")
        return Response(status=status.HTTP_200_OK,
                        template_name='main/mypage.html',
                        data={'my_post': my_post, 'user_post': my_user_post, 'nickname': user.nickname})

class Select_post_Revise(LoginRequiredMixin, APIView): # 예약 게시글 수정
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request, pk):
        if request.user.nickname == '':
            return redirect('main:Main_check')
        check = pk_check(pk, 1)
        if check == False:
            post = Post.objects.get(id=pk)
            form = Post_check(instance=post)
            day = datetime.now()
            min_day = str(day.date())
            return Response(status=status.HTTP_200_OK, template_name='main/Revise_write.html',
                            data={'form': form, 'pk': pk,
                                  'min_day': min_day})
        else:
            return redirect('main:list')

    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        form = Post_check(post, data=request.data, context={'request': request, 'Revise': 1})
        day = datetime.now()
        min_day = str(day.date())
        if form.is_valid():
            form.save()
            messages.success(request, "게시글이 수정되었습니다.")
            road_check(request.user, "{}번째 예약 게시판 수정".format(pk))
            return redirect('main:posts', pk)
        else:
            return Response(status=status.HTTP_200_OK, template_name='main/Revise_write.html', data={'form': form, 'pk': pk,
                                                                                                 'min_day': min_day})

class Select_post_del(LoginRequiredMixin, APIView): # 예약 게시글 삭제
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request, pk):
        if request.user.nickname == '':
            return redirect('main:Main_check')
        check = pk_check(pk, 1)
        if check == False:
            post = Post.objects.get(id=pk)
            user = Users.objects.get(nickname=request.user)
            user.post_num -= 1
            if user.post_num < 2:
                user.post_limit = False
            user.save()
            post.remove = True
            post.save()
            messages.success(request, "게시글이 삭제되었습니다.")
            road_check(request.user, "{}번째 예약 게시판 삭제".format(pk))
            return redirect('main:list')
        else:
            return redirect('main:list')

class Select_main(LoginRequiredMixin, APIView):  #메인 페이지 @수정 완
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        if request.user.nickname == '':
            return redirect('main:Main_check')
        else:
            road_check(request.user, "메인 페이지")
            nickname = request.user
            post = Post.objects.filter(clear=False, remove=False, Done=False)
            # posts = user.users.all()  # 예약 유저 역참조
            # reservation_post = posts.exclude(car_user=request.user)  # 본인을 제외한 나머지 게시글
            # try:
            #     check_reservation_post = reservation_post[0]  # 첫번째 값
            # except:
            #     check_reservation_post = False
            my_post = Post.objects.filter(car_user=request.user, clear=False, remove=False, Done=False)  # 예약 정보
            recent_posts = post.order_by('-create_date')[:1]  # 최근 글
            recent_mypost = my_post.order_by('date')[:1]
            user_post = user_reservation.objects.filter(remove=False)
            recent_user = user_post.order_by('-create_date')[:1]  # 최근 글
            recent_get_id = recent_posts.values('id')
            recent_user_get_id = recent_user.values('id')
            return Response(status=status.HTTP_200_OK,
                            data={
                                "recent_mypost": recent_mypost,
                                "nickname": nickname,
                                "recent_posts": recent_posts,
                                "recent_userpost": recent_user,
                                "recent_get_id" : recent_get_id,
                                "recent_user_get_id" : recent_user_get_id,
                                # "check_reservation_post": check_reservation_post,
                                }
                                ,template_name='main/select_main.html')

class Main_check(LoginRequiredMixin, APIView): #유저 닉네임이 없다면 새로 설정 @수정 완
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        return Response(status=status.HTTP_200_OK, template_name='account/nickname_add.html')

    def post(self, request):
        user = Users.objects.get(email=request.user)
        form = Account_check(user, data=request.data)
        if form.is_valid():
            form.save()
            return redirect('main:select_main')
        else:
            return Response(status=status.HTTP_200_OK, template_name='account/nickname_add.html', data={'form': form})

class User_post_list(LoginRequiredMixin, APIView): # 유저 게시판 리스트

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        if request.user.nickname == '':
            return redirect('main:Main_check')
        forms = user_reservation.objects.filter(remove=False)
        form = forms.order_by('-create_date')
        road_check(request.user, "유저 게시판")
        return Response(status=status.HTTP_200_OK, template_name='main/user_main.html',
                        data={'board_lists': forms})

class User_post_make(LoginRequiredMixin, APIView): # 유저 게시판 만들기
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        if request.user.nickname == '':
            return redirect('main:Main_check')
        day = datetime.now()
        min_day = str(day.date())
        return Response(status=status.HTTP_200_OK, template_name='main/user_write.html', data={'min_day': min_day})

    def post(self, request):
        form = user_reservation_check(data=request.data, context={'request_user': request.user})
        day = datetime.now()
        min_day = str(day.date())
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, "게시글이 등록되었습니다.")
            road_check(request.user, "유저 게시판 생성")
            return redirect('main:user_list')
        else:
            return Response(status=status.HTTP_200_OK, template_name='main/user_write.html', data={'min_day': min_day})
class User_post(LoginRequiredMixin, APIView): #선택한 유저 게시글
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk):
        if request.user.nickname == '':
            return redirect('main:Main_check')
        check = pk_check(pk, 2)
        if check == False:
            post = user_reservation.objects.get(id=pk)
            user = request.user
            post_list = post.comment_user.all()
            post_lists = post_list.filter(clear=False, remove=False)
            road_check(request.user, "{}번째 유저 게시판".format(pk))
            return Response(status=status.HTTP_200_OK,
                            template_name='main/user_post.html',
                            data={'post': post, 'pk': pk, 'post_list': post_lists, 'user': user})
        else:
            return redirect('main:user_list')

    def post(self, request, pk):
        user = request.user
        select_post = Post.objects.filter(car_user=request.user, clear=False, remove=False)
        try:
            post2 = select_post[1]
        except:
            post2 = 0
        try:
            post1 = select_post[0]
        except:
            post1 = 0
        road_check(request.user, "{}번째 유저 게시판의 차추 추천".format(pk))
        return Response(status=status.HTTP_200_OK,
                        template_name='main/select_post.html',
                        data={'post1': post1, 'post2': post2, 'pk': pk, 'user': user})

class Select_post(LoginRequiredMixin, APIView): # 유저 게시판에 초대 보내기
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    def post(self, request, pk):
        check = pk_check(pk, 2)
        if check == False:
            select_posts = Post.objects.filter(car_user=request.user, clear=False, remove=False)
            post = user_reservation.objects.get(id=pk)
            num = int(request.data['num']) - 1
            select_post = select_posts[num]
            post.comment_user.add(select_post)
            user = request.user
            post_list = post.comment_user.all()
            post_lists = post_list.filter(clear=False, remove=False)
            return Response(status=status.HTTP_200_OK,
                            template_name='main/user_post.html',
                            data={'post': post, 'pk': pk, 'post_list': post_lists, 'user': user})
        else:
            return redirect('main:user_list')

class User_post_del(LoginRequiredMixin, APIView): # 유저 게시글 삭제
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request, pk):
        if request.user.nickname == '':
            return redirect('main:Main_check')
        check = pk_check(pk, 2)
        if check == False:
            post = user_reservation.objects.get(id=pk)
            post.remove = True
            post.save()
            messages.success(request, "게시글이 삭제되었습니다.")
            road_check(request.user, "{}번째 유저 게시판 삭제".format(pk))
            return redirect('main:user_list')
        else:
            return redirect('main:user_list')

class User_Revise(LoginRequiredMixin, APIView): # 유저 게시글 수정
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request, pk):
        if request.user.nickname == '':
            return redirect('main:Main_check')
        check = pk_check(pk, 2)
        if check == False:
            post = user_reservation.objects.get(id=pk)
            form = user_reservation_check(instance=post)
            day = datetime.now()
            min_day = str(day.date())
            return Response(status=status.HTTP_200_OK, template_name='main/user_Revise_write.html',
                            data={'form': form, 'pk': pk,
                                  'min_day': min_day})
        else:
            return redirect('main:user_list')

    def post(self, request, pk):
        post = user_reservation.objects.get(id=pk)
        form = user_reservation_check(post, data=request.data)
        day = datetime.now()
        min_day = str(day.date())
        if form.is_valid():
            form.save()
            messages.success(request, "게시글이 수정되었습니다.")
            road_check(request.user, "{}번째 유저 게시판 수정".format(pk))
            return redirect('main:user_list')
        else:
            return Response(status=status.HTTP_200_OK, template_name='main/user_Revise_write.html', data={'form': form, 'pk': pk,
                                                                                                 'min_day': min_day})
class Clears(LoginRequiredMixin, APIView): # 예약 게시판 종료  @ 수정
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request, pk):
        if request.user.nickname == '':
            return redirect('main:Main_check')
        post = Post.objects.get(id=pk)
        post.clear=True
        level_up = Level.objects.get(id=1) # @ 수정 레벨업
        level_up.level_num += 1
        level_up.save()
        post.save()
        user = Users.objects.get(nickname=request.user)
        user.post_num -= 1
        if user.post_num < 2:
            user.post_rock = False
        user.save()
        road_check(request.user, "{}번째 유저 게시판 성공".format(pk))
        return redirect('main:list')


class Post_filter(LoginRequiredMixin, APIView): # 수정
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        if request.user.nickname == '':
            return redirect('main:Main_check')
        day = datetime.now()
        min_day = str(day.date())
        return Response(status=status.HTTP_200_OK,
                        template_name='main/sort_test.html', data={'today': min_day})

    def post(self, request):
        min_price = request.data['min_price'] # 최소 가격
        max_price = request.data['max_price']  # 최대 가격
        date = request.data['date'] # 날짜
        region = request.data['region'] # 지역
        print(min_price,max_price,date,region)
        q = Q()
        if max_price and min_price:
            q.add(Q(money__range=[min_price, max_price]), q.AND)
        if date:
            q.add(Q(date=date), q.AND)
        if region:
            q.add(Q(end_region=region), q.AND)

        first_filter = Post.objects.filter(q)
        order = request.GET.get('order') # 정렬 옵션
        last_filter = first_filter.order_by('-create_date')
        if order == 1:   # 최신순
            last_filter = first_filter.order_by('-create_date')
        elif order == 2:  # 날짜 빠른순
            last_filter = first_filter.order_by('date')
        elif order == 3:  # 날짜 느린순
            last_filter = first_filter.order_by('-date')
        elif order == 4:  # 저가순
            last_filter = first_filter.order_by('money')
        elif order == 5:  # 고가순
            last_filter = first_filter.order_by('-money')

        car = Users.objects.get(nickname=request.user)
        user = request.user

        return Response(status=status.HTTP_200_OK, template_name='main/main.html',
                        data={'board_lists': last_filter, 'car': car, 'user': user})

class Modify(LoginRequiredMixin, APIView): # 유저 정보 수정
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        if request.user.nickname == '':
            return redirect('main:Main_check')
        user = Users.objects.get(nickname=request.user)
        user_modify = Account_check(instance=user)
        return Response(status=status.HTTP_200_OK, template_name='main/modify.html',
                                data={'user_modify': user_modify})
    def post(self, request):
        user = Users.objects.get(nickname=request.user)
        user_modify = Account_check(user, data=request.data)
        if user_modify.is_valid():
            user_modify.save()
            return Response(status=status.HTTP_200_OK, template_name='main/modify.html',
                            data={'user_modify': user_modify})
        else:
            return Response(status=status.HTTP_200_OK, template_name='main/modify.html',
                            data={'user_modify': user_modify})

def post_detail_view(request):
    post = Post.objects.all()
    post = post.order_by('-create_date')
    post = post[:1]

    return render(request, "main/trash/detail_test.html",
                  {
                      "post" : post,
                  })
