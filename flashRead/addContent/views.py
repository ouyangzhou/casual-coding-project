from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
import datetime
import os

from users.models import User
from books.models import Book
from chapters.models import Chapter
# Create your views here.

def myWorks(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/users/login/?next=%s' % request.path)
	else:
		template = loader.get_template('addContent/myInfo.html')
		userid = request.user #User.objects.get(pk=uid)
		bookList = Book.objects.filter(author=request.user) #This is the list of books this user has written
		bookList = bookList.order_by('date_updated').reverse()
		context = RequestContext(request, {'bookList': bookList, 'userid': userid} )
		return HttpResponse(template.render(context))

def addBook(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/users/login/?next=%s' % request.path)
	else:
		template = loader.get_template('addContent/addBook.html')
		userid = request.user
		context = RequestContext(request, {'userid': userid})

		if (request.method == 'POST'):
			new_work = Book(
				title = request.POST['title'],
				genre = request.POST['genre'],
				category = request.POST['category'],
				abstract = request.POST['abstract'],
				warning = False, # Is it 18+?
				wordcount = 0,
				hits = 0,
				votes = 0,
				date_updated = datetime.datetime.now(),
				status = request.POST['status'],
				author = request.user
				)
			new_work.save()
			
			return HttpResponseRedirect(reverse('addContent:myWorks'))

		else:
			return HttpResponse(template.render(context))

		return HttpResponse(template.render(context))

def editBook(request, bid):
	book = Book.objects.get(pk=bid)
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/users/login/?next=%s' % request.path)
	elif (request.user == book.author):
		template = loader.get_template('addContent/editBook.html')
		chapterList = Chapter.objects.filter(book=bid) #This is the list of chapters in one work
		chapterList = chapterList.order_by('chapter_number')
		userid = request.user
		context = RequestContext(request, {'chapterList': chapterList, 'book': book, 'uid': userid} )

		if request.POST.get('editBook'):
			book.title = request.POST['title']
			book.genre = request.POST['genre']
			book.category = request.POST['category']
			book.abstract = request.POST['abstract']
			book.status = request.POST['status']
			book.warning = False # Is it 18+?
			book.save()
			return HttpResponseRedirect(reverse('addContent:myWorks'))

		elif request.POST.get('deleteBook'):
			# remove all chapter files and delete book entry
			dirpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/'))
			if (os.path.exists(dirpath)):
				for chapter in chapterList:
					os.remove(os.path.join(dirpath, chapter.file_location));
				Book.objects.filter(bid=bid).delete()
				return HttpResponseRedirect(reverse('addContent:myWorks'))
			else:
				return HttpResponse("An error has occured! Dirpath not found: " + dirpath)

		else:
			return HttpResponse(template.render(context))

		return HttpResponse(template.render(context))
	else:
		return HttpResponse("Access Denied.")

def addChapter(request, bid):
	book = Book.objects.get(pk=bid)
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/users/login/?next=%s' % request.path)
	elif (request.user == book.author):
		template = loader.get_template('addContent/addChapter.html')
		userid = request.user
		context = RequestContext(request, {'uid': userid, 'book': book})

		if (request.method == 'POST'):
			dirpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/'))
			if (os.path.exists(dirpath)):
				new_chapter = Chapter(
					title = request.POST['title'],
					chapter_number = request.POST['chapter_number'],
					file_location = "",
					wordcount = 0,
					date_updated = datetime.datetime.now(),
					book = Book.objects.get(pk=bid),
					)
				new_chapter.save()

				filename = str(bid)+"_"+str(new_chapter.chid)+".txt"

				new_chapter.file_location = filename
				new_chapter.save()

				# write content into text file
				text_file = open(os.path.join(dirpath, new_chapter.file_location), "w", encoding="utf-8")
				text_file.write(request.POST['content'])
				text_file.close()

				# find word count
				text_file = open(os.path.join(dirpath, new_chapter.file_location), "r", encoding="utf-8")
				# create a list of all words fetched from the file using a list comprehension
				words = [word for line in text_file for word in line.split()]
				text_file.close()

				new_chapter.wordcount = len(words)
				new_chapter.save()

				# update book's last updated
				book.date_updated = new_chapter.date_updated

				# update book's word count
				chapterList = Chapter.objects.filter(book=bid)
				book.wordcount = 0
				for ch in chapterList:
					book.wordcount += ch.wordcount

				book.save()

			else:
				return HttpResponse("An error has occured! Dirpath not found: " + dirpath)
				
			return HttpResponseRedirect(reverse('addContent:editBook', kwargs={'bid': bid}))

		else:
			return HttpResponse(template.render(context))

		return HttpResponse(template.render(context))
	else:
		return HttpResponse("Access Denied.")

def editChapter(request, bid, chid):
	book = Book.objects.get(pk=bid)
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/users/login/?next=%s' % request.path)
	elif (request.user == book.author):
		template = loader.get_template('addContent/editChapter.html')
		chapter = Chapter.objects.get(pk=chid)
		userid = request.user
		data = ""

		dirpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/'))
		if (os.path.exists(dirpath)):
			text_file = open(os.path.join(dirpath, chapter.file_location), "r", encoding="utf-8")
			data = text_file.read().replace("\n\n", "\n")
			text_file.close()
		else:
			return HttpResponse("An error has occured! Dirpath not found: " + dirpath)

		context = RequestContext(request, {'chapter': chapter, 'book': book, 'uid': userid, 'data': data} )
		#text_file.close()
		
		if request.POST.get('editChapter'):
			if (os.path.exists(dirpath)):
				chapter.title = request.POST['title']
				chapter.chapter_number = request.POST['chapter_number']
				chapter.date_updated = datetime.datetime.now()
				chapter.save()

				# write content into text file
				text_file = open(os.path.join(dirpath, chapter.file_location), "w", encoding="utf-8")
				text_file.write(request.POST['content'])
				text_file.close()

				# find word count
				text_file = open(os.path.join(dirpath, chapter.file_location), "r", encoding="utf-8")
				# create a list of all words fetched from the file using a list comprehension
				words = [word for line in text_file for word in line.split()]
				text_file.close()
				
				chapter.wordcount = len(words)
				chapter.save()

				# update book's last updated
				book.date_updated = chapter.date_updated

				# update book's word count
				chapterList = Chapter.objects.filter(book=bid)
				book.wordcount = 0
				for ch in chapterList:
					book.wordcount += ch.wordcount

				book.save()

			else:
				return HttpResponse("An error has occured! Dirpath not found: " + dirpath)

			return HttpResponseRedirect(reverse('addContent:editBook', kwargs={'bid': bid}))

		elif request.POST.get('deleteChapter'):
			# remove chapter file and delete chapter entry
			os.remove(os.path.join(dirpath, chapter.file_location));
			Chapter.objects.filter(chid=chid).delete()

			# update book's word count
			chapterList = Chapter.objects.filter(book=bid)
			book.wordcount = 0
			for ch in chapterList:
				book.wordcount += ch.wordcount
			book.save()
			
			return HttpResponseRedirect(reverse('addContent:editBook', kwargs={'bid': bid}))

		else:
			return HttpResponse(template.render(context))

		return HttpResponse(template.render(context))
	else:
		return HttpResponse("Access Denied.")