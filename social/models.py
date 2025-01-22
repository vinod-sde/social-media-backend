from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Post(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    content=models.TextField(max_length=280)
    created_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.author.username}:{self.content[:20]}"

class Follower(models.Model):
    follower=models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")
    following=models.ForeignKey(User,on_delete=models.CASCADE,related_name="followers")
    class Meta:
        unique_together=("follower","following")

class UserAction(models.Model):
    ACTION_CHOICES=[
        ('HIDE','Hide'),
        ('BLOCK','Block'),
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="actions")
    target_user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="targeted_actions")
    action=models.CharField(max_length=5,choices=ACTION_CHOICES)
    class Meta:
        unique_together=("user","target_user")