from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=100)
    slug = models.CharField(max_length=130)
    timeStamp = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title + " - " + self.author

class Comment(models.Model):
    sno = models.AutoField(primary_key=True)
    blogComment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # On which post the comment is done and on delete means if post or user is deleted, delete the comment too
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # For the replies to know the parent comment
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timeStamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.blogComment[0:13] + "... by " + self.user.username
    
