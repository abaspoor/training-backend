from django.db import models
from django.contrib.auth.models import User, UserManager

def upload_path_handler(instance, filename):
    return "avatars/{id}/{file}".format(id=instance.user.id, file=filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_path_handler, blank=True)
    is_premium = models.BooleanField(default=False)
    bio = models.CharField(max_length=256,blank=True, null=True)

class Location(models.Model):
    user = models.OneToOneField(User,related_name='location',on_delete=models.CASCADE)
    location = models.CharField(max_length=100,blank=True,null=True)

class Group(models.Model):
    name = models.CharField(max_length=32, null=False, unique=False)
    location = models.CharField(max_length=32, null=False)
    description = models.CharField(max_length=256, null=False, unique=False)

    class Meta:
        unique_together = (('name','location'))

class Event(models.Model):
    team1 = models.CharField(max_length=32 , blank= False)
    team2 = models.CharField(max_length=32, blank=False)
    time = models.DateTimeField(null=False , blank=False)
    score1 = models.IntegerField(null=True , blank=True)
    score2 = models.IntegerField(null=True, blank=True)
    group = models.ForeignKey(Group,related_name='events', on_delete=models.CASCADE)


class Member(models.Model):
    group = models.ForeignKey(Group,related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='memeber_of', on_delete=models.CASCADE)
    admin = models.BooleanField(default=False)
    class Meta:
        unique_together= (('user','group'),)
        index_together = (('user', 'group'),)


class Comment(models.Model):
    group = models.ForeignKey(Group,related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(Group, related_name='user_comments', on_delete=models.CASCADE)
    description = models.CharField(max_length=256,null=False, unique=False)
    time = models.DateTimeField(auto_now_add=True)