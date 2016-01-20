'''
Created on 20-Jan-2016

@author: minion
'''
from __builtin__ import str
from django.db import IntegrityError, transaction
from django.http import *
from django.template.context import RequestContext
import json

from .models import Transaction , User


def is_user_exists(id):
    """
    check if the user id exist in the user table for validation.
    """
    try:
        if id is None or len(str(id)) == 0:
            return False
        user_model = User.objects.filter(pk=id)
        if user_model is not None and len(user_model) >= 1:
            return True
        else:
            return False;
    except Exception , e:
        print(e)
        return None;

def send(request):
    """
    Controller function which send messages from one user to another.
    """
    try:
        must_have = set()
        if request.method == 'GET':
            if 'from' in request.GET:
                sender_id = int(str(request.GET['from']))
            else:
                must_have.add('from')
            if 'to' in request.GET:
                receiver_id = int(str(request.GET['to']))
            else:
                must_have.add('to')
            if 'msg' in request.GET:
                message = str(request.GET['msg'].encode('utf-8'))
            else:
                must_have.add('msg')
        elif request.method == 'POST':
            if 'from' in request.POST:
                sender_id = int(str(request.POST['from']))
            else:
                must_have.add('from')
            if 'to' in request.POST:
                receiver_id = int(str(request.POST['to']))
            else:
                must_have.add('to')
            if 'msg' in request.POST:
                message = str(request.POST['msg'].encode('utf-8'))
            else:
                must_have.add('msg')
        else:
            return_data = dict({'status':201 , 'message' : "Invalid request protocol"})
            return HttpResponse(json.dumps(return_data), content_type='application/json')
        
        if len(must_have) > 0:
            return_data = dict({'status':201 , 'message' : "Parameter not present : " + ",".join(must_have)})
            return HttpResponse(json.dumps(return_data), content_type='application/json')
        
        if is_user_exists(sender_id) is not True:
            return_data = dict({'status':201 , 'message' : "sender id do not exist"})
            return HttpResponse(json.dumps(return_data), content_type='application/json')
        
        if is_user_exists(receiver_id) is not True:
            return_data = dict({'status':201 , 'message' : "receiver id do not exist"})
            return HttpResponse(json.dumps(return_data), content_type='application/json')
        
        transaction_model = Transaction()
        transaction_model.sender = sender_id
        transaction_model.receiver = receiver_id
        transaction_model.message = message
        transaction_model.status = 0
        transaction_model.save()
        return_data = dict({'status':200, 'message' : "Successfully Sent"})
    except Exception, e:
        print(e)
        return_data = dict({'status':201 , 'message' : "Some error occurred"})
    return HttpResponse(json.dumps(return_data), content_type='application/json')

def get_new_messages(request):
    """
    get all the new messages from a user < optional parameter > for a user
    """
    try:
        if request.method == 'GET':
            if 'user_id' in request.GET:
                user_id = int(str(request.GET['user_id']))
            else:
                return_data = dict({'status':201 , 'message' : "Parameter not present : user_id"})
                return HttpResponse(json.dumps(return_data), content_type='application/json')   
            if 'from_id' in request.GET:
                from_id = int(str(request.GET['from_id'])) 
            else:
                from_id = None
        elif request.method == 'POST':
            if 'user_id' in request.POST:
                user_id = int(str(request.POST['user_id']))
            else:
                return_data = dict({'status':201 , 'message' : "Parameter not present : user_id"})
                return HttpResponse(json.dumps(return_data), content_type='application/json')
            if 'from_id' in request.POST:
                from_id = int(str(request.POST['from_id']))
            else:
                from_id = None
        else:
            return_data = dict({'status':201 , 'message' : "Invalid request protocol"})
            return HttpResponse(json.dumps(return_data), content_type='application/json')
        
        if is_user_exists(user_id) is not True:
                return_data = dict({'status':201 , 'message' : "user id do not exist"})
                return HttpResponse(json.dumps(return_data), content_type='application/json')
        messages = []
        #making transaction atomic
        with transaction.atomic():
            if from_id:
                new_transactions = Transaction.objects.filter(receiver=user_id).filter(sender=from_id).filter(status=0).all()
            else:
                new_transactions = Transaction.objects.filter(receiver=user_id).filter(status=0).all()
            for item in new_transactions:
#                 new_transactions.status = 1
                Transaction.objects.filter(pk=item.id).update(status=1)
                messages.append(str(item.message))
        if len(messages) > 0:
            return_data = dict({'status':200 , 'message':messages})
        else:
            return_data = dict({'status':200 , 'message':"No new messages"})
    except Exception, e:
        print(e)
        return_data = dict({'status':201 , 'message' : "Some error occurred"})
    return HttpResponse(json.dumps(return_data), content_type='application/json')
