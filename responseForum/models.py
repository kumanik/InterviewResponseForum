from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)

class InterviewResponse(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    profile = models.CharField(max_length=200)
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    rounds = models.IntegerField(blank=True, null=True)
    questions = models.TextField(max_length=1000000)
    review = models.CharField(max_length=1000000)
    offer = models.IntegerField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    hits = models.IntegerField(default=0)

    def __str__(self):
        return str('{} at {}'.format(self.profile, self.company))

    def increase(self):
        self.hits += 1
        self.save()

class responseView(models.Model):
    response = models.ForeignKey(InterviewResponse, on_delete=models.CASCADE)
    ip = models.CharField(max_length=200, null=True)
    session = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(default=timezone.now)

class Comment(models.Model):
    response = models.ForeignKey(InterviewResponse, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return "Comment {} by {}".format(self.body, self.username)