from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


from users.forms import UserCreateForm, UserProfileForm
from users.models import UserProfile
from books.models import Book
from chapters.models import Chapter

@login_required
def edit_profile(request):
    form = UserProfileForm()
    if request.method == "POST": 
        instance=request.user.profile
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/users/profile')
    else:
        u = request.user
        profile = u.profile
        form = UserProfileForm(instance=profile)
    return render(request, 'users/edit_profile.html', {'form': form})


def profile(request):
    return render(request, 'users/profile.html')


def favouriteBooks(request):
    if request.user.is_authenticated():
        userprofile=request.user.profile
        favouriteBooks=userprofile.favorites.all()
        context = {'user':request.user, 'favouriteBooks':favouriteBooks}
        return render(request, 'users/favouriteBooks.html', context)
    else:
        return redirect('/users/login')
def deleteFavourite(request, book_id):
    if request.method!='POST':
        return redirect('/users/login')
    
    if request.user.is_authenticated():
        userprofile=request.user.profile
        deleteBook=Book.objects.filter(bid=book_id)
        userprofile.favorites.remove(deleteBook[0])
        
        favouriteBooks=userprofile.favorites.all()
        #favouriteBooks.save()
        context = {'user':request.user, 'favouriteBooks':favouriteBooks}
        return render(request, 'users/favouriteBooks.html', context)
    else:
        return redirect('/users/login')
def bookmarkChapters(request):
    if request.user.is_authenticated():
        userprofile=request.user.profile
        bookmark=userprofile.bookmark.all()
        context = {'user':request.user, 'bookmark':bookmark}
        return render(request, 'users/bookmark.html', context)
    else:
        return redirect('/users/login')
def deleteBookmark(request, chapter_id):
    if request.method!='POST':
        return redirect('/users/login')
    
    if request.user.is_authenticated():
        userprofile=request.user.profile
        deleteChapter=Chapter.objects.filter(chid=chapter_id)
        userprofile.bookmark.remove(deleteChapter[0])
        
        bookmark=userprofile.bookmark.all()
        #favouriteBooks.save()
        context = {'user':request.user, 'bookmark':bookmark}
        return render(request, 'users/bookmark.html', context)
    else:
        return redirect('/users/login')
def register(request):
    form = UserCreateForm()
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(username=form.cleaned_data['username'],email= form.cleaned_data['email'],password=form.cleaned_data['password1'])
            return HttpResponseRedirect('/users/register_success')
    else:
        form = UserCreateForm() 
    return render(request, 'users/register.html', {'form': form}) 

def register_success(request):
    return render(request, 'users/register_success.html')

