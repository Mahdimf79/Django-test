from django.db import models

class Question(models.Model):
    text=       models.CharField(max_length=300)
    pub_date=   models.DateTimeField()

    def __str__(self):
        return self.text


class Choice(models.Model):
    question=   models.ForeignKey(Question, on_delete=models.CASCADE)
    text=       models.CharField(max_length=300)
    vote=       models.IntegerField(default=0)

    def __str__(self):
        return self.text
