from django.db import models
from django.utils import timezone
from uuid import uuid4

class Question(models.Model):
    text=       models.CharField(max_length=500)
    pub_date=   models.DateTimeField('date published')

    def __str__(self):
        return self.text


class Choice(models.Model):
    question=   models.ForeignKey(Question, on_delete=models.CASCADE)
    text=       models.CharField(max_length=500)
    vote=       models.IntegerField(default=0)

    def __str__(self):
        return self.text


class Username(models.Model):
    def create_id():
        nows = timezone.now()
        return str(nows.year)+str(nows.month)+str(nows.day)+str(uuid4())[:7]

    id = models.CharField(primary_key=True, default=create_id, editable=False, max_length= 1000)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=64)
    firstname = models.CharField(max_length=30)
    lastname= models.CharField(max_length=30)
    email = models.CharField(max_length=254)
