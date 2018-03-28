from django.db import models
 
from users.models import User
from chapters.models import Chapter
 
# Create your models here.
class Comment(models.Model):
	coid = models.AutoField(primary_key=True)
	content = models.CharField(max_length=255)
	date_updated = models.DateTimeField(auto_now=True, auto_now_add=True)
	commentor = models.ForeignKey(User)
	chapter = models.ForeignKey(Chapter)
 
	def __str__(self):
		return (self.commentor.username)