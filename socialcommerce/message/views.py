from django.shortcuts import render

# Create your views here.

def message_list(request):
    return render(request, 'message/message_list.html', {})

def single_message(request):
    return render(request, 'message/message_list.html', {})

def get_message(request):
    pass

def send_message(request):
    pass