from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,UpdateAPIView,DestroyAPIView

from drf_yasg.utils import swagger_auto_schema
from .serializer import RegisterSerializer

User = get_user_model()


class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer())
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)


class ActivationView(APIView):
    
    def get(self, request, email, activation_code):
        user = User.objects.filter(email=email, activation_code=activation_code).first()
        if not user:
            return Response('пользаватель не найден', 404)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('Вы успешно активировали аккаунт', 200)
    






