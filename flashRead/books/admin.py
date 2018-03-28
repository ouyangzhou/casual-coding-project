from django.contrib import admin

from books.models import Book
admin.site.register(Book)

from chapters.models import Chapter
admin.site.register(Chapter)

from users.models import UserProfile
admin.site.register(UserProfile)

from comments.models import Comment
admin.site.register(Comment)