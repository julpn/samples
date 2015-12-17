from __future__ import unicode_literals

from django.db import models

from django.db import models

class Member(models.Model):
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	date_added = models.DateField(auto_now_add=True)
	birthday = models.DateField()
	favorite_ice_cream = models.CharField(max_length=100)
