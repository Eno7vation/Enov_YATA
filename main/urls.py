from django.urls import path, include

from . import views
from .views import Post_make, Post_list, Select_Post, Reservation_searched, My_page,Select_post_Revise,\
    Select_post_del, Select_main, User_post_list, User_post_make, User_post, Select_post, User_post_del, User_Revise,Clears, Main_check, Post_filter, Modify
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
app_name = 'main'

urlpatterns = [
    path('make/', Post_make.as_view(), name='make'), # 예약 게시글 만들기
    path('list/', Post_list.as_view(), name='list'), # 예약 게시글 리스트
    path('<int:pk>/post/', Select_Post.as_view(), name='posts'), # 선택한 예약 게시글
    path('main/post/searched/', Reservation_searched.as_view(), name='search'), # 예약 게시글 찾기
    path('main/mypage/', My_page.as_view(), name='my_page'), # 마이 페이지
    path('<int:pk>/Revise/', Select_post_Revise.as_view(), name='Revise'), # 예약 게시글 수정
    path('<int:pk>/delete/', Select_post_del.as_view(), name='delete'), # 예약 게시글 삭제
    path('', Select_main.as_view(), name='select_main'), # 유저, 차주 게시판 선택
    path('user_list/', User_post_list.as_view(), name='user_list'), # 유저 게시판 리스트
    path('user_make/', User_post_make.as_view(), name='user_post_make'), # 유저 게시판 만들기
    path('<int:pk>/user_post/', User_post.as_view(), name='user_post'), # 선택한 유저 게시판
    path('<int:pk>/select_post/', Select_post.as_view(), name='select_post'), # 유저 게시판에 넣는 초대 예약 게시판
    path('<int:pk>/user_delete/', User_post_del.as_view(), name='user_delete'), # 유저 게시판 삭제
    path('<int:pk>/user_Revise/', User_Revise.as_view(), name='user_Revise'), # 유저 게시판 수정
    path('<int:pk>/post_clears/', Clears.as_view(), name='clears'), # 예약 게시판 완료
    path('main_Check/', Main_check.as_view(), name='Main_check'),  # 처음 회원가입을 한 경우 이동하는 페이지 @수정 완
    path('list/filter/', Post_filter.as_view(), name='Post_filter'), #필터 @추가
    path('modify/', Modify.as_view(), name='Modify'), # 정보 변경
    #########################################
    path('test/', views.post_detail_view),
    path('board/', TemplateView.as_view(template_name="main/trash/noticeboard.html")),
    ]

