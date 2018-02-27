# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.


class User_manager(models.Manager):
	def basic_validation(self, postData):
		errors = {}
		if len(postData['first_name']) < 2:
			errors["first_name"] = "first name should be at least 2 characters"
		if len(postData['last_name']) < 2:
			errors["last_name"] = "last name should be at least 2 characters"
		if not EMAIL_REGEX.match(postData['email']):
			errors["email"] = "email must match standard email format"
		if len(postData['password']) < 8:
			errors['password'] = "password needs to be at least 8 characters"
		return errors

class Users(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = User_manager()

class Authors(models.Model):
	auth_name = models.CharField(max_length=255)
	Users = models.ForeignKey(Users, related_name="Authors")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

class Books(models.Model):
	title = models.CharField(max_length=255)
	author = models.ForeignKey(Authors, related_name="Books")
	Users = models.ForeignKey(Users, related_name="Books")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

class Reviews(models.Model):
	review = models.TextField()
	rating = models.IntegerField()
	rate_type = models.CharField(max_length=255)
	books = models.ForeignKey(Books, related_name="Books")
	users = models.ForeignKey(Users, related_name="Reviews")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
