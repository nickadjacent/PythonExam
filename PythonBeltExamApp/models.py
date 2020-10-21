from django.db import models
from django.contrib import messages
import re


class UserManager(models.Manager):
    def user_validator(self, post_data):
        user_errors = {}
        if len(post_data['first_name']) < 3:
            user_errors['first_name'] = 'First Name should be at least 3 characters.'
        if len(post_data['last_name']) < 3:
            user_errors['last_name'] = 'Last Name should be at least 3 characters.'
        Email_Regex = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not Email_Regex.match(post_data['email']):
            user_errors['email'] = 'Invalid email address.'
        if len(post_data['email']) < 3:
            user_errors['email'] = 'Email should be at least 3 characters.'
        if len(post_data['password']) < 8:
            user_errors['password'] = 'Password should be at least 8 characters'
        if post_data['password_confirm'] != post_data['password']:
            user_errors['password_confirm'] = 'Passwords do not match.'
        return user_errors


class AuthorManager(models.Manager):
    def author_validator(self, post_data):
        author_errors = {}
        if len(post_data['name']) < 3:
            author_errors['name'] = "Author's name should be at least 3 characters"
        if len(post_data['quote']) < 10:
            author_errors['quote'] = "Quote should be at least 10 characters."
        return author_errors


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Author(models.Model):
    name = models.CharField(max_length=30)
    quote = models.TextField()
    user = models.ForeignKey(
        "User", related_name="user_name", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AuthorManager()
    users_who_liked = models.ManyToManyField(
        "User", related_name="liked_quote")
