from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password_hash = models.CharField(max_length=60)
    description = models.CharField(max_length=100)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=100)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=100)

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_by')