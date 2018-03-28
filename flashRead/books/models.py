from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    bid = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, default=1)
     
    title = models.CharField(max_length=50, default='')
    genre = models.CharField(max_length=50, default='')
    category = models.CharField(max_length=100, default='')
    abstract = models.CharField(max_length=255, default='')
    
    warning = models.BooleanField(default=True) # Is it 18+?
    wordcount = models.IntegerField(default=0)
    hits = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    date_updated = models.DateTimeField('date published', default='2011-01-01')
    status = models.CharField(max_length=50, default='')

    def __str__(self):
        return (self.title)
    