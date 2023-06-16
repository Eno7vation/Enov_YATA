from django.urls import path
from .views import Logout
app_name = 'account'

urlpatterns = [
    path('logout/', Logout.as_view(), name='logout'),

]