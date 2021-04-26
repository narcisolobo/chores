from django.db import models
import re

class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_data['full_name']) < 2:
            errors['full_name'] = 'Full name must be at least two characters.'
        if len(post_data['email_address']) < 1:
            errors['email_address'] = 'Please enter your email address.'
        if not EMAIL_REGEX.match(post_data['email_address']):
            errors['email_valid'] = 'Please enter a valid email.'
        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least eight characters.'
        if len(post_data['password']) >= 8:
            if post_data['password'] != post_data['password_confirm']:
                errors['password_no_match'] = 'Passwords do not match.'
        return errors

    def login_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_data['login_email']) < 1:
            errors['login_email'] = 'Please enter your email address.'
        if not EMAIL_REGEX.match(post_data['login_email']):
            errors['login_email_valid'] = 'Please enter a valid email.'
        if len(post_data['login_password']) < 1:
            errors['login_password'] = 'Please enter your password.'
        return errors

class User(models.Model):
    full_name = models.CharField(max_length=45)
    email_address = models.CharField(max_length=45)
    password = models.CharField(max_length=60)
    # created_chores - a list of the user's created chores
    # assigned_chores - a list of the user's assigned chores
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class ChoreManager(models.Manager):
    def chore_validator(self, post_data):
        errors = {}
        if len(post_data['name']) < 1:
            errors['name'] = 'Please enter chore name.'
        return errors

class Chore(models.Model):
    name = models.CharField(max_length=45)
    creator = models.ForeignKey(User, related_name='created_chores', on_delete=models.CASCADE)
    assignees = models.ManyToManyField(User, related_name='assigned_chores')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ChoreManager()