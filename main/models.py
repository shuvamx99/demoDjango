import imp
from tabnanny import verbose
from tkinter import CASCADE
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class QuizCategory(models.Model):
    title = models.CharField(max_length=100)
    detail = models.TextField()
    image = models.ImageField(upload_to = 'imgs/')

    class Meta:
        verbose_name_plural ='Categories'

    def __str__(self):
        return self.title
    
class QuizQuestions(models.Model):
    category = models.ForeignKey(QuizCategory,on_delete=models.CASCADE)# on deleting this category question will get deleted as well
    question = models.TextField()
    opt_1 = models.CharField(max_length=100)
    opt_2 = models.CharField(max_length=100)
    opt_3 = models.CharField(max_length=100)
    opt_4 = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    time_limit = models.IntegerField()
    right_opt = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Questions'


    def __str__(self):
        return self.question


class UserSubmittedAnswer(models.Model):
    question = models.ForeignKey(QuizQuestions,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    right_answer = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'User Submitted Answers'




    


