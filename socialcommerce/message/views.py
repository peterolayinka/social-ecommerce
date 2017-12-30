from django.utils import timezone

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import JsonResponse

from store.models import Store
from .serializers import UnreadMessageSerializer
from .models import Message, MessageList
# Create your views here.


User = get_user_model()

def message_list(request):
    if 'store' in request.path:
        message_lists = MessageList.objects.filter(
            Q(store=request.user.store_owned))
        return render(request, 'message/store_message.html', {'message_lists': message_lists})
    message_lists = MessageList.objects.filter(
        Q(user_from=request.user) | Q(user_to=request.user))
    return render(request, 'message/message_list.html', {'message_lists':message_lists})

def single_message(request, receipient_id, message_list=None):
    if 'store' in request.path:
        receipient = get_object_or_404(User, pk=receipient_id)
    else:
        receipient = get_object_or_404(Store, pk=receipient_id)

    messages = None
    message_items = None
    if 'store' in request.path:
        message_lists = MessageList.objects.filter(
            Q(store=request.user.store_owned))
    else:
        message_lists = MessageList.objects.filter(
            Q(user_from=request.user) | Q(user_to=request.user))
    try:
        if 'store' in request.path:
            message_list = MessageList.objects.get(
                store=request.user.store_owned, user_from=receipient).id
        else:
            message_list = MessageList.objects.get(store=receipient, user_from=request.user).id
    except:
        pass
    
    if message_list:
        if 'store' in request.path:
            message_items = Message.objects.filter(Q(
                message_list_id=message_list, user_from=receipient) | 
                Q(message_list_id=message_list, user_to=receipient))
            unread_messages = Message.objects.filter(message_list_id=message_list, store=request.user.store_owned)
        else:
            message_items = Message.objects.filter(
                message_list_id=message_list, store=receipient)
            unread_messages = Message.objects.filter(Q(message_list_id=message_list, user_from=request.user) | Q(
                message_list_id=message_list, user_to=request.user))

        for message in unread_messages:
            if request.user == message.user_from:
                message.user_from_read = True
            elif 'store' in request.path:
                message.store_read = True
            else:
                message.user_to_read = True
            message.save()

        if unread_messages:
            message_list_read = unread_messages.first().message_list
            if request.user == message.user_from:
                message_list_read.user_from_read = True
            elif 'store' in request.path:
                message_list_read.store_read = True
            message_list_read.save()
    
    if 'store' in request.path:
        message_template_name = 'message/store_message.html'
    else:
        message_template_name = 'message/message_list.html'
    return render(request, message_template_name, {'message_lists': message_lists,
                                                        'receipient': receipient,
                                                        'message_list_id': message_list,
                                                         'message_items': message_items})

def get_message(request, receipient_id=None, message_list_id=None):
    sender = None
    if 'store' in request.path:
        message_unread = Message.objects.filter(Q(message_list_id=message_list_id, store_read=False))
        if message_unread:
            sender = message_unread.first().store.name
    else:
        message_unread = Message.objects.filter(Q(store_id=receipient_id, user_from=request.user, user_from_read=False) | 
                                            Q(store_id=receipient_id, user_to=request.user, user_to_read=False))
        sender = request.user
    serializer = UnreadMessageSerializer(message_unread, many=True)
    # import pdb; pdb.set_trace()
    for message in message_unread:
        print(message.content)
        if 'store' in request.path:
            message.store_read = True
        elif request.user == message.user_from:
            message.user_from_read = True
        else:
            message.user_to_read = True
        message.save()
    # import pdb; pdb.set_trace()
    return JsonResponse({'status': True, 'messages': serializer.data, 
                            'sender': str(sender)}, safe=True)

def send_message(request, receipient_id=None, message_list_id=None):
    data = request.POST
    # import pdb; pdb.set_trace()
    # store = Store.objects.get(pk=data['store-id'])
    try:
        if 'store' in request.path:
            message_list = MessageList.objects.get(store=request.user.store_owned, user_from_id=data['user-id'])
        else:
            message_list = MessageList.objects.get(store_id=receipient_id, user_from=request.user)
    except:
        message_list = MessageList.objects.create(user_from=request.user, store_id=data['store-id'])

    if 'store' in request.path:
        message = Message.objects.create(user_to_id=data['user-id'], store_id=data['store-id'], message_list=message_list, content=data['message'], from_store=True)
    else:
        message = Message.objects.create(user_from=request.user, store_id=data['store-id'], message_list=message_list, content=data['message'])
    message_list.store_read = False
    message_list.created = timezone.now()
    message_list.save()
    return JsonResponse({'status': True})
