from django.urls import path

from . import views

app_name = "tech"

urlpatterns = [
    ##############################################################################
    #Post Read, Create Views.py
    path('', views.index, name='index'),
    path('main/<str:category>/', views.first, name='first'),
    path('post/<int:pk>/', views.seconds, name='post_detail'),
    path('post/<int:post_pk>/comment/new/', views.comment_new, name='comment_new'),
    ##############################################################################
    #Follow Views.py
    path('post/<int:pk>/like/', views.post_like, name='post_like'),
    path('post/<int:pk>/unlike/', views.post_unlike, name='post_unlike'),

    ##############################################################################
    #Follow Views.py
    path('donate/', views.donate, name='donate'),
    path('test/', views.test),

    ##############################################################################
    #Bug Read, Create Views.py
    path('search/', views.bug_search, name="bug_search"),
    path('bug_report/', views.bug_report, name="bug_report"),
    path('bug_report/modify/<int:pk>/', views.bug_report_modify, name="bug_report_modify"),
    path('bug_report/delete/<int:pk>/', views.bug_report_delete, name="bug_report_delete"),
    path('bug_success/', views.bug_report_success, name="bug_success"),
    path('conditions/', views.conditions, name="conditions"),
    path('conditions_personal/', views.conditions_personal, name="conditions_personal"),
    ##############################################################################
    ]
