#coding=utf-8
from __future__ import unicode_literals

from django.db import models

import datetime
from django.contrib.auth.models import User
from django import forms


class AESSLIST(models.Model):
	name = models.CharField(max_length=50)
	ip = models.CharField(max_length=50)
	env = models.CharField(max_length=50)
	createtime = models.DateTimeField(auto_now_add=True)
	status = models.BigIntegerField(default=0)
	


def __unicode__(self):
    return self.username

