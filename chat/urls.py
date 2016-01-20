'''
Created on 20-Jan-2016

@author: minion
'''
from django.conf.urls import url

from . import views


urlpatterns = [
    url('send', views.send, name='send'),
    url('get', views.get_new_messages, name='get'),
]