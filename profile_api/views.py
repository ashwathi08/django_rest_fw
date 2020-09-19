from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from rest_framework import status
from rest_framework import viewsets
from . import models
from . import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated


# Create your views here.

class HelloApiView(APIView):
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        an_apiview = [
            'im ashwathi',
            'im a developer'
        ]
        return Response({'message': 'Hello', 'an_apiview': an_apiview})

    def post(self, request):
        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = "Hello", name
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        return Response({'message': 'Put'})

    def patch(self, request, pk=None):
        return Response({'message': 'Patch'})

    def delete(self, request, pk=None):
        return Response({'message': 'Delete'})


class HelloViewset(viewsets.ViewSet):
    """"Viewset api"""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        a_viewapi = [
            'this is a viewset api',
            'perfect fr std db operations',
        ]
        return Response({
            'message': 'Hello',
            'a_viewapi': a_viewapi
        })

    def create(self, request):

        serializer = serializers.HelloSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello', name
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        return Response({'Http_Method': 'Get'})

    def update(self, request, pk=None):
        return Response({'Http_Method': 'Update'})

    def partial_update(self, request, pk=None):
        return Response({'Http_Method': 'partial update'})

    def destroy(self, request, pk=None):
        return Response({'Http_Method': 'Delete'})


class UserProfileViewset(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    # authentication_classes = (TokenAuthentication,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class LoginViewset(viewsets.ViewSet):
    """check email and password and return authtoken"""
    serializer_class = AuthTokenSerializer

    def create(self, request):
        """use obtainauthtoken APIViewto validate and return token"""
        return ObtainAuthToken().post(request)


class ProfileFeedViewset(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items."""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user."""
        serializer.save(user_profile=self.request.user)