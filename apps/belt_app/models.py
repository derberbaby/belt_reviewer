# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
import re
import datetime
import dateutil.relativedelta
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
	def register(self, data):
		messages = []

		for field in data:
			if len(data[field]) == 0:
				fields = {
					'name':'Name',
					'alias':'Alias',
					'email':'Email',
					'password':'Password',
					'confirm':'Confirmation password',
					'birthday':'Birthday'
				}
				messages.append(fields[field]+' must be filled in')

		if len(data['name']) < 2:
			messages.append('Name must be at least two characters long')

		# if data['name'].isalpha()==False:
		# 	messages.append('Name must only contain letters')

		if not EMAIL_REGEX.match(data['email']):
			messages.append('Must enter a valid email')

		try:
			User.objects.get(email=data['email'])
			messages.append('Email already registered')
		except:
			pass

		if len(data['password']) < 8:
			messages.append('Password must be at least eight characters long')

		# if re.search('[0-9]', data['password']) is None:
		# 	messages.append('Password must contain at least one number')
		#
		# if re.search('[A-Z]', data['password']) is None:
		# 	messages.append('Password must contain at least one capital letter')

		if data['password'] != data['confirm']:
			messages.append('Password and confirmation password must match')

		if data['birthday']:
			birthday = datetime.datetime.strptime(data['birthday'], '%Y-%m-%d')
			now = datetime.datetime.now()
			age = dateutil.relativedelta.relativedelta(now, birthday)

			if birthday > now:
				messages.append('Pick a date in the past')
			if age.years < 18:
				messages.append('Must be at least 18 years old to register')

		if len(messages) > 0:
			return messages
		else:
			hashed_pw=bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
			new_user= User.objects.create(name=data['name'], alias=data['alias'], email=data['email'], hashed_pw=hashed_pw, birthday=data['birthday'])
			return new_user.id

	def login(self, data):
		messages = []
		for field in data:
			if len(data[field]) == 0:
				fields = {
					'email':'Email',
					'password':'Password'
				}
				messages.append(fields[field]+' must be filled in')

		try:
			user = User.objects.get(email=data['email'])
			encrypted_pw = bcrypt.hashpw(data['password'].encode(), user.hashed_pw.encode())
			if encrypted_pw==user.hashed_pw.encode():
				return user.id
			else:
				messages.append('Wrong password')
		except:
			messages.append('User not registered')

		if len(messages) > 0:
			return messages

class User(models.Model):
	name = models.CharField(max_length=250)
	alias = models.CharField(max_length=250)
	email = models.CharField(max_length=250)
	hashed_pw = models.CharField(max_length=250)
	birthday = models.DateField()
	friend = models.ManyToManyField("self")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects=UserManager()

class Book(models.Model):
	title = models.CharField(max_length=255)
	favorited_by = models.ManyToManyField(User, related_name='favorite_books')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class ReviewManager(models.Manager):
	def add(self, data, user_id):
		messages = []

		if len(data['new_auth'])==0 and data['author']=='':
			messages.append('Must provide at least one author')

		if len(data['comment']) == 0:
			messages.append('Cannot leave blank review')

		if data['rating']=='':
			messages.append('Please give a rating')

		if len(messages)==0:
			try:
				book = Book.objects.get(title = data['title'])
				user = User.objects.get(id=user_id)

				try:
					author = Author.objects.get(name = data['author'])
					author.books.add(book)
				except:
					if len(data['new_auth']) > 0:
						author = Author.objects.create(name = data['new_auth'])
						author.books.add(book)

				review = Review.objects.create(user = user, rating = data['rating'], comment = data['comment'], book = book)
			except:
				book = Book.objects.create(title = data['title'])

				try:
					author = Author.objects.get(name = data['author'])
					author.books.add(book)
				except:
					if len(data['new_auth']) > 0:
						author = Author.objects.create(name = data['new_auth'])
						author.books.add(book)

				user = User.objects.get(id=user_id)
				review = Review.objects.create(user = user, rating = data['rating'], comment = data['comment'], book = book)
			return book.id
		else:
			return messages

	def review_book(self, data, user_id, book_id):
		messages = []

		if len(data['comment'])==0:
			messages.append('Cannot leave a blank review')
		if data['rating']=='':
			messages.append('Please give a rating')
		else:
			book = Book.objects.get(id=book_id)
			user = User.objects.get(id=user_id)
			try:
				review = Review.objects.get(book=book, user=user)
				messages.append("You've already reviewed this book")
			except:
				review = Review.objects.create(rating = data['rating'], comment = data['comment'], user = user, book = book)
				return review

		if len(messages) > 0:
			return messages

class Review(models.Model):
	rating = models.IntegerField()
	comment = models.CharField(max_length=255)
	user = models.ForeignKey(User, related_name='all_reviews')
	book = models.ForeignKey(Book, related_name='book_reviews')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects=ReviewManager()

class Author(models.Model):
	name = models.CharField(max_length=255)
	books = models.ManyToManyField(Book, related_name='book_authors')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
