from urllib import response

from django.shortcuts import render
from rest_framework import viewsets,generics,permissions,status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view

class StandardResultsPagination(PageNumberPagination):
    page_size=10
    
class PostViewSet(viewsets.ModelViewSet):
    queryset=Post.objects.all().order_by('-created_at')
    serializer_class=PostSerializer
    permission_classes=[permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
class FollowUserView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request,username):
        try:
            target_user=User.objects.get(username=username)
            if target_user == request.user:
                return Response({"detail":"you cannot follow yourself,"},status=status.HTTP_400_BAD_REQUEST)
            Follower.objects.create(follower=request.user,following=target_user)
            return Response({"detail":f"you are now following{username}."},status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"detail":"user not found"},status=status.HTTP_404_NOT_FOUND)
            
class UnfollowUserView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request,username):
        try:
            target_user=User.objects.get(username=username)
            Follower.objects.filter(follower=request.user,following=target_user).delete()
            return Response({"detail":f"you have unfollwed{username}."})
        except User.DoesNotExist:
            return Response({"detail":"user not found"},status=status.HTTP_404_NOT_FOUND)
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = StandardResultsPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        hidden_users = UserAction.objects.filter(user=self.request.user, action='HIDE').values_list('target_user', flat=True)
        blocked_users = UserAction.objects.filter(user=self.request.user, action='BLOCK').values_list('target_user', flat=True)
        followed_users = Follower.objects.filter(follower=self.request.user).values_list('following', flat=True)
        return Post.objects.filter(author__id__in=followed_users).exclude(author__id__in=hidden_users | blocked_users)

# Create your views here.
