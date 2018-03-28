from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

import os
import datetime
from django.conf.urls import patterns, url, include

from chapters.models import Chapter
from books.models import Book
from comments.models import Comment

def detail(request, chapter_id):
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    dirpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/'))

    if (os.path.exists(dirpath)):
        f = open(os.path.join(dirpath, chapter.file_location), "r", encoding="utf-8")
        content=[]
        for line in f:
            content.append(line)
        #content = f.readlines()
        #content=''
        #with f as fp:
            #for line in fp:
                #content=content+'/n'+line
        f.close()
    else:
        return HttpResponse("An error has occured! Dirpath not found: " + dirpath)

    #get previous and next chapter if applicable
    bookChapter = Chapter.objects.filter(book=chapter.book)

    index=0
    found=False
    while index<bookChapter.count() and found==False:
        item=bookChapter.order_by('chapter_number')[index]
        if item.pk==chapter.pk:
            index=index
            found=True
        else:
            index=index+1
            
    previous=0
    if index!=0:
        previousChapter=bookChapter.order_by('chapter_number')[index-1]
        previous=previousChapter.pk

    after=0
    if index!=bookChapter.count()-1:
        nextChapter=bookChapter.order_by('chapter_number')[index+1]
        after=nextChapter.pk

    #check if user is logged in. If yes, allow editing if user is the author of the book
    login=False
    current_user=request.user
    current_user_id = request.user.id
    if request.user.is_authenticated():
        login=True
    else:
        login=False

    book=chapter.book
    bookId=book.pk
    #book=get_object_or_404(Book, bid=bookId)
    #if login==True:
    commentList = Comment.objects.filter(chapter=chapter).order_by('date_updated').reverse()
    
    context = {'chapter': chapter, 'content': content, 'previous': previous, 'next': after, 'bookId':bookId, 'login':login, 'commentList':commentList}


    if (request.method == 'POST'):
            new_comment = Comment(
                content = request.POST['content'],
                date_updated = datetime.datetime.now(),
                commentor = current_user,
                chapter = chapter,
                )
            new_comment.save()

    return render(request, 'chapters/detail.html', context)
def bookmark(request, chapter_id):
    if request.method!='POST':
        return redirect('/books')

    if request.user.is_authenticated():
        chapter = get_object_or_404(Chapter, pk=chapter_id)
        userprofile=request.user.profile
        #userprofile=UserProfile.objects.filter(myuser=request.user)
        checkIfBookmarked=False
        if userprofile!=None:
            for bookmark in userprofile.bookmark.all():
                if bookmark == chapter:
                    checkIfBookmarked=True
            else:
                userprofile.save()
                userprofile.bookmark.add(chapter)
                userprofile.save()
        else:
            userprofile=UserProfile(myuser=request.user)
            userprofile.save()
            userprofile.bookmark.add(chapter)
            userprofile.save()

        success=True
        if checkIfBookmarked==False:
            success=True
        else:
            success=False
        context = {'user': request.user, 'chapter': chapter, "success": success}
        return render(request, 'chapters/bookmark.html', context)
    else:
        return redirect('/users/login')
