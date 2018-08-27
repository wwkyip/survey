from django.db import models

# Create your models here.


class UserData(models.Model):
    uname = models.CharField(max_length=200)
    label = models.CharField(max_length=500)
    ratings = models.IntegerField(default=0)
    insertime = models.DateTimeField(auto_now_add=True)

