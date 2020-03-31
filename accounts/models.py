from django.db import models
from django.contrib.auth.models import User
from responseForum.models import Company
import datetime


YEAR_CHOICES = []
for r in range(1980, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((str(r),str(r)))
YEAR_CHOICES.append(("Present","Present"))

class Employment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    profile = models.CharField(max_length=40)
    start  = models.CharField(max_length=7, choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    end  = models.CharField(max_length=7, choices=YEAR_CHOICES, default=datetime.datetime.now().year)


class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institute = models.CharField(max_length=50)
    degree = models.CharField(max_length=50)
    start  = models.CharField(max_length=7, choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    end  = models.CharField(max_length=7, choices=YEAR_CHOICES, default=datetime.datetime.now().year)