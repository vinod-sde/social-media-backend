from django.shortcuts import render
from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Post, Follower, UserAction
from .serializers import PostSerializer, UserActionSerializer
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

# Pagination Class
class StandardResultsPagination(PageNumberPagination):
    page_size = 10

# Post Management
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Follow a User
class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        try:
            target_user = User.objects.get(username=username)
            if target_user == request.user:
                return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
            Follower.objects.create(follower=request.user, following=target_user)
            return Response({"detail": f"You are now following {username}."}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

# Unfollow a User
class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        try:
            target_user = User.objects.get(username=username)
            Follower.objects.filter(follower=request.user, following=target_user).delete()
            return Response({"detail": f"You have unfollowed {username}."})
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

# Feed View
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = StandardResultsPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        hidden_users = UserAction.objects.filter(user=self.request.user, action='HIDE').values_list('target_user', flat=True)
        blocked_users = UserAction.objects.filter(user=self.request.user, action='BLOCK').values_list('target_user', flat=True)
        followed_users = Follower.objects.filter(follower=self.request.user).values_list('following', flat=True)
        return Post.objects.filter(author__id__in=followed_users).exclude(author__id__in=hidden_users | blocked_users)

# Authentication Views
@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
        if not user.check_password(password):
            return Response({'error': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

# Hide/Block Actions
class UserActionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        action = request.data.get('action')
        if action not in ['HIDE', 'BLOCK']:
            return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_user = User.objects.get(username=username)
            if target_user == request.user:
                return Response({'error': 'You cannot perform this action on yourself.'}, status=status.HTTP_400_BAD_REQUEST)

            UserAction.objects.create(user=request.user, target_user=target_user, action=action)
            return Response({'detail': f'{action} action applied to {username}.'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, username):
        try:
            target_user = User.objects.get(username=username)
            UserAction.objects.filter(user=request.user, target_user=target_user).delete()
            return Response({'detail': f'Action removed for {username}.'})
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
