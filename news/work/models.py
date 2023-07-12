from django.db import models
from django import forms

# Create your models here.

class News(models.Model):
    news_name = models.CharField(max_length=200)
    news_desc = models.TextField()
    news_img = models.ImageField(upload_to='new')
    news_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-news_date']





