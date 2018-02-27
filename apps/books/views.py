# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from models import *
import bcrypt

# Create your views here.
def login_page(request):
	return render(request, 'books/login.html')

def books_page(request):
	#run a query to pull up books.
	all_books = Books.objects.order_by("created_at")
	# 3_books = (all_books[0], all_books[1], all_books[2])
	all_reviews = Authors.objects.all()
	context = {
	'books': all_books,
	'reviews': all_reviews
	}
	return render(request, 'books/books.html', context)

def add_book_page(request):
	all_authors = Authors.objects.all()
	context = {
		'authors': all_authors
	}
	return render(request, 'books/add_books.html', context)

def each_book_page(request, id):
	book = Books.objects.get(id=id)
	reviews = Reviews.objects.filter(books=Books.objects.get(id=id))
	context = {
	'book': book,
	'reviews': reviews
	}
	return render(request, 'books/each_book.html', context)

def add_review(request, id):
	book_id = id
	user_id = request.session['id']
	book1 = Books.objects.get(id=book_id)
	user = Users.objects.get(id=user_id)
	review = request.POST['review']
	rating = request.POST['rating_num']
	rate_type = request.POST['rating_type']
	Reviews.objects.create(review=review, rating=rating, rate_type=rate_type, books=book1, users=user)
	return redirect('/books/'+id)

def users(request, id):
	user = Users.objects.get(id=id)
	books = Books.objects.filter(Users=user)
	context = {
	'user': user,
	'books': books
	}
	return render(request, 'books/user.html', context)

def add_book_review(request):
	user_id = request.session['id']
	auth_id = 0
	#add author or get author
	if request.POST['add_author'] != None:
		author = request.POST['add_author']
		Authors.objects.create(auth_name=author, Users=Users.objects.get(id=user_id))
		auth_id = Authors.objects.last()
		auth_id = auth_id.id
	else:
		auth_id = int(request.POST['author'])
		auth_id = Authors.objects.get(id=auth_id)
	#add book
	title = request.POST['title']
	Books.objects.create(title=title, author=Authors.objects.get(id=auth_id), Users=Users.objects.get(id=user_id))
	#add review
	review = request.POST['review']
	rating = request.POST['rating_num']
	rate_type = request.POST['rating_type']
	Reviews.objects.create(review=review, rating=rating, rate_type=rate_type, books=Books.objects.get(title=title), users=Users.objects.get(id=user_id))
	return redirect('/books')

def register(request):
	if request.method == "POST":
		errors = Users.objects.basic_validation(request.POST)
		if len(errors):
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
				return redirect('/')
		if request.POST['password'] != request.POST['password2']:
			messages.error(request, "Bro, passwords need to match")
			return redirect('/')
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		alias = request.POST['alias']
		email = request.POST['email']
		pw = request.POST['password']
		hash_pw = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
		# password = request.POST['password']
		Users.objects.create(first_name=first_name, last_name=last_name, alias=alias, email=email,password=hash_pw)
		messages.error(request,"Registration accepted! Please log in.")
		return redirect('/')
	else:
		return redirect('/')

def login(request):
	log_email = request.POST['log_email']
	log_passw = request.POST['log_password']
	query = Users.objects.filter(email=log_email)
	if len(query) != 0:
		stord_pw = query[0].password
		if bcrypt.checkpw(log_passw.encode(), stord_pw.encode()) == False:
			messages.error(request, "Bro, that ain't your password")
			return redirect('/')
		else:
			#session log in
			request.session['id'] = query[0].id
			# print ('session id is ' + str(request.session['id']))#for testing purposes
			messages.error(request,"session log in")
			return redirect('/books')
	else:
		messages.error(request, "Bro, we can't find your account.")
		return redirect('/')
	

def log_out(request):
	#session log out
	request.session.clear()
	# messages.clear()
	return redirect('/')