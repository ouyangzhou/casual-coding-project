from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
import datetime
from datetime import timedelta

from books.models import Book
from users.models import UserProfile
from chapters.models import Chapter

def index(request):
    book_list = Book.objects.all()
    context = {'book_list': book_list}
    return render(request, 'books/booklist.html', context)

def login_user_view(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.hits+=1
    book.save()
    
    chapter_list = Chapter.objects.filter(book = book_id)

    
    context = {'book': book, 'chapter_list': chapter_list}
    return render(request, 'books/login_user_view.html', context)


#@login_required
def favourite(request, book_id):
    if request.method!='POST':
        return redirect('/books')

    if request.user.is_authenticated():
        book = get_object_or_404(Book, pk=book_id)
        userprofile=request.user.profile
        #userprofile=UserProfile.objects.filter(myuser=request.user)
        checkIfFavourite=False
        if userprofile!=None:
            for favourite in userprofile.favorites.all():
                if favourite == book:
                    checkIfFavourite=True
            else:
                userprofile.save()
                userprofile.favorites.add(book)
                userprofile.save()
        else:
            userprofile=UserProfile(myuser=request.user)
            userprofile.save()
            userprofile.favorites.add(book)
            userprofile.save()

        success=True
        if checkIfFavourite==False:
            success=True
        else:
            success=False
        context = {'user': request.user, 'book': book, "success": success}
        return render(request, 'books/favourite.html', context)
    else:
        return redirect('/users/login')
def search(request):
    if request.method!='POST':
        return redirect('/books')
    searchType = request.POST['searchtype']

    if searchType=='category':
        userInput = request.POST["searchcategoryType"]
    elif searchType=='genre':
        userInput = request.POST['searchgenre']
    else:
        userInput = request.POST['searchuserInput']
        userInput = userInput.lower()
    
    bookList=[]
    if searchType == 'bookName':
        for book in Book.objects.all():
            if userInput in book.title.lower():
                bookList.append(book)
        #bookList = Book.objects.filter(title=userInput)
    elif searchType == 'category':
        bookList = Book.objects.filter(category=userInput)
    elif searchType == 'genre':
        bookList = Book.objects.filter(genre=userInput)
    elif searchType == 'author':
        #matchingUsers=User.objects.filter(username=userInput)
        userIdList=[]
        for user in User.objects.all():
            if userInput in user.username.lower():
                userIdList.append(user.pk)
        if len(userIdList)!=0:
            bookList=Book.objects.filter(author=userIdList[0])
            for userId in userIdList:
                authorBook=Book.objects.filter(author=userId)
                bookList=bookList | authorBook
    
    context = {'book_list': bookList}
    return render(request, 'books/searchResult.html', context)
def goToAdvSearch(request):
    context = {'book_list': Book}
    return render(request, 'books/advSearch.html', context)
def advSearch(request):
    if request.method!='POST':
        return redirect('/books')
    #searchType = request.POST['type']

    bookKey=request.POST['bookname'].lower()
    authorKey=request.POST['authorname'].lower()
    category=request.POST['categoryType']
    genre=request.POST['genre']
    status=request.POST['status']
    
    bookList=[]
    userIdList=[]
    for user in User.objects.all():
        if authorKey in user.username.lower():
            userIdList.append(user.pk)
    if len(userIdList)!=0:
        for book in Book.objects.all():
            #first by book name and author by key words
            if bookKey in book.title.lower() and book.author.pk in userIdList:
                #General means not specified, return all
                #if specified, only return specified
                if status=='General':
                    if category=='General' and genre=='General':
                        bookList.append(book)
                    elif category=='General' and genre!='General':
                        if book.genre==genre:
                            bookList.append(book)
                    elif category!='General' and genre=='General':
                        if book.category==category:
                            bookList.append(book)
                    else:
                        if book.genre==genre and book.category==category:
                            bookList.append(book)
                else:
                    if book.status==status:
                        if category=='General' and genre=='General':
                            bookList.append(book)
                        elif category=='General' and genre!='General':
                            if book.genre==genre:
                                bookList.append(book)
                        elif category!='General' and genre=='General':
                            if book.category==category:
                                bookList.append(book)
                        else:
                            if book.genre==genre and book.category==category:
                                bookList.append(book)
    
    context = {'book_list': bookList}
    return render(request, 'books/searchResult.html', context)
def vote(request, book_id):
    if request.user.is_authenticated():
        book = get_object_or_404(Book, pk=book_id)
        userprofile=request.user.profile
        vote_made=userprofile.vote_of_day
        vote_time=userprofile.vote_time

        haveVoteLeft=False
        if vote_made<2:
            userprofile.vote_of_day+=1
            userprofile.save()
            haveVoteLeft=True
        else:
            now=datetime.datetime.now()
            day_difference=now.day-vote_time.day
            hour_difference=now.hour-vote_time.hour
            if day_difference*24+hour_difference>=24:
                userprofile.vote_of_day=1
                userprofile.vote_time=datetime.datetime.now()
                userprofile.save()
                haveVoteLeft=True
            else:
                haveVoteLeft=False
        if haveVoteLeft==True:
            book.votes+=1
            book.save()
        user=request.user
        context = {'user': user, 'book': book, 'success':haveVoteLeft}
        return render(request, 'books/voteResult.html', context)
    else:
        return redirect('/users/login')
