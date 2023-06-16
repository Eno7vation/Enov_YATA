from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render
from introduce.models import Level

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
#########################소개 페이지###############################
def about(request):
    level = Level.objects.all()
    first = str(level[0])
    first = int(first[0])
    sec = first + 1
    return render(request, "introduce/about_us.html",
                  {
                      "level" : level,
                      "first" : first,
                      "sec" : sec,
                  })

def stack(request):
    return render(request, "introduce/stack.html")

def guide(request):
    return render(request, "introduce/guide.html")

# def intro(request):
#     return render(request, "introduce/trash_html/intro.html")
#
# def contact(request):
#     return render(request, "introduce/trash_html/contact.html")

#########################소개 페이지###############################

#########################베타 테스터, 운전자 지원페이지###############################
# def apply_create(request):
#     if request.method == "POST":
#         form = ApplyForm(request.POST, request.FILES)
#         if form.is_valid():
#             apply = form.save(commit=False)
#             apply.author = request.user
#             apply.save()
#             messages.success(request, '포스팅 저장했습니다.')
#             return redirect('introduce:contact')
#     else:
#         form = ApplyForm()
#     return render(request, 'introduce/trash_html/apply_form.html',
#                   {
#                       'form': form,
#                   })
#
# def tester_apply_create(request):
#     if request.method == "POST":
#         form = DriverApplyForm(request.POST, request.FILES)
#         if form.is_valid():
#             apply = form.save(commit=False)
#             apply.author = request.user
#             apply.save()
#             messages.success(request, '포스팅 저장했습니다.')
#             return redirect('introduce:contact')
#     else:
#         form = DriverApplyForm()
#     return render(request, 'introduce/trash_html/tester_apply_form.html',
#                   {
#                       'form': form,
#                   })
# #########################베타 테스터, 운전자 지원페이지###############################
#
# #########################Redis TEST###############################
# @cache_page(CACHE_TTL)
# @login_required()
# def test_redis_apply(request):
#     apply_list = Apply.objects.all()
#     return render(request, 'introduce/trash_html/redis_test.html',
#                   {
#                       "apply_list" : apply_list,
#                   })
#
# @cache_page(CACHE_TTL)
# @login_required()
# def redis_key_value(request):
#     apply = cache.get('apply')
#     if not apply:
#         apply = list(Apply.objects.all().values('id', 'author', 'caption'))
#         cache.set("apply", apply)
#     return JsonResponse(apply, safe=False)
#
# def current_location(request):
#     return render(request, "introduce/trash_html/currentlocation.html")
# def test_kakao(request):
#     return render(request, "introduce/test_kakao.html")
#
# def test_kakao2(request):
#     return render(request, "introduce/cal_location.html")
# #########################Redis TEST###############################
# def road(request):
#     return render(request, "introduce/road.html")
#
# def search(request):
#     return render(request, "introduce/search.html")

