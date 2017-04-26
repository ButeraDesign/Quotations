from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):

    def emailIsValid(self, postData):
        print 'IN emailIsValid'
        if len(postData) < 1 or not EMAIL_REGEX.match(postData):
            return False
        return True

    def pwMatch(self, password, hashed):
        encpw = password.encode('utf-8')
        encHash = hashed.encode('utf-8')

        if bcrypt.hashpw(encpw, encHash) == encHash:
            return True
        else:
            return False

    def pwIsValid(self, postDataPW1, postDataPW2):
        print 'IN pwIsValid'
        if len(postDataPW1) < 8 :
            return False
        if postDataPW2 !=  postDataPW1:
            return False
        return True

    def ckFirstName(self, postDataFn):
        print 'ckFirstName'
        if len(postDataFn) < 2 or not NAME_REGEX.match(postDataFn):
            return False
        return True

    def ckLastName(self, postDataLn):
        print 'ckLastName'
        if len(postDataLn) < 2 or not NAME_REGEX.match(postDataLn):
            return False
        return True

class Users(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Quotes(models.Model):
    message = models.CharField(max_length=256)
    quotedBy = models.CharField(max_length=64)
    user = models.ForeignKey(Users)
    favorites = models.ManyToManyField(Users, related_name="allFavs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
