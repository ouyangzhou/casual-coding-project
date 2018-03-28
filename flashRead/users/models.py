from django.db import models
from django.contrib.auth.models import User
import datetime
# from django.db.models.signals import post_save
from books.models import Book
from chapters.models import Chapter


class UserProfile(models.Model):  
    myuser = models.OneToOneField(User)
    about = models.CharField(max_length=255) 
	
    GENDER_CHOICES=(
        ('Male', 'Male'),
        ('Female', 'Female'),
        ("It's a secret. Shh..", "It's a secret. Shh.."),
        ('Others', 'Others'),
    )
    gender = models.CharField(max_length=140, choices=GENDER_CHOICES)
	
    #vote_of_day = models.IntegerField(default=5)
	
    favorites = models.ManyToManyField(Book, related_name='favorited_by', default='')
    bookmark = models.ManyToManyField(Chapter, related_name='bookmark', default='')
    vote_of_day = models.IntegerField(default=0)
    vote_time=models.DateTimeField(default=datetime.datetime.utcnow())

    def __unicode__(self):
        return u'Profile of myuser: %s' % self.myuser.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(myuser=u)[0])

