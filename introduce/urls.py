from django.urls import path

from introduce import views

app_name = "introduce"

urlpatterns = [
    #############################USE########################################
    path('about/', views.about, name = "about"),
    path('stack/', views.stack, name="stack"),
    path('guide/', views.guide , name="guide"),
    #############################USE########################################
    # path('intro/', views.intro, name = "intro"),
    # path('contact/', views.contact, name = "contact"),
    # path('contact/apply_create/', views.apply_create, name="apply_create"),
    # path('contact/tester_create/', views.tester_apply_create, name="tester_apply_create"),
    # path('testc/', views.current_location, name="current_location"),
    # path('testd/', views.test_redis_apply, name="test_redis_apply"),
    # path('teste/', views.redis_key_value, name="redis_key_value"),
    # path('q/', views.test_kakao, name = "test_kakao"),
    # path('qq/', views.test_kakao2, name= "test_kakao2"),
    # path('road/', views.road, name="road"),
]