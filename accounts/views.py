from django.shortcuts import redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from main.views import road_check
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.mixins import LoginRequiredMixin


class Logout(LoginRequiredMixin, APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request):
        road_check(request.user, "로그아웃")
        logout(request)
        return redirect('account:login')




