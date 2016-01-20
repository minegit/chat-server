from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import default


class User(models.Model):
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        managed = True
        db_table = 'user'
        
class Transaction(models.Model):
    sender = models.IntegerField(default=-1)
    receiver = models.IntegerField(default=-1)
    message = models.TextField()
    status = models.IntegerField(default=0)
    
    class Meta:
        managed = True
        db_table = 'transaction'
    
