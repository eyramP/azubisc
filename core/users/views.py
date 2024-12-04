from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import RetrieveUpdateAPIView
from .serializers import UserSerializer, RegisterAdminUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CustomUserDetailsView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return get_user_model().objects.none()


class RegisterAdminUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args):
        data = request.data
        serializer = RegisterAdminUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'success': 'Admin account created successfully'}, status=status.HTTP_201_CREATED)
