""" accounts/views.py """
from django.shortcuts import render, HttpResponse
from accounts.models import CustomUser
from accounts.serializers import (
    CustomUserSerializer, UserAuthTokenSerializer, ChangePasswordSerializer, MessageSerializer
)
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class CustomUserAPIView(generics.CreateAPIView):
    """
    API through which any user can register
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginAPIView(ObtainAuthToken):
    """
    API through which registered user can login
    """
    serializer_class = UserAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserAuthTokenSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            response_data = {
                'email' : user.email,
                'token' : token.key
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(generics.UpdateAPIView):

    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    # def get_object(self, request):
    #     import pdb; pdb.set_trace()
    #     token = Token.objects.get(key=request.auth.key)
    #     return token.user

    def update(self, request, *args, **kwargs):
        user = self.get_object(request)



class GetMessageAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer

    def get_object(self):
        import pdb; pdb.set_trace()
        token = Token.objects.get(key=request.auth.key)
        return CustomUser.objects.get(id=user_id)

    def get(self, request, *args, **kwargs):
        import pdb; pdb.set_trace()
        user = self.get_object()
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
