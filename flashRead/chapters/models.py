from django.db import models

from books.models import Book

class Chapter(models.Model):
    chid = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book)
    
    title = models.CharField(max_length=50)
    
    file_location = models.CharField(max_length=255)
    chapter_number = models.IntegerField()
    wordcount = models.IntegerField()
    date_updated = models.DateTimeField('date added')

    def __str__(self):
        return (self.title)