from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('users/<str:username>/follow/', FollowUserView.as_view()),
    path('users/<str:username>/unfollow/', UnfollowUserView.as_view()),
    path('feed/', FeedView.as_view()),
]
