from django.db.models import Q
from .models import Order
from message.models import Message


def order(request):
    awaiting_order_count = Order.objects.filter(
        store=request.user.store_owned, status=Order.AWAITING).count()
    store_message_count = Message.objects.filter(
        store=request.user.store_owned, store_read=False).count()
    user_message_count = Message.objects.filter(
        Q(user_from=request.user, user_from_read=False) | Q(user_to=request.user, user_to_read=False)).count()
    store_activity_count = awaiting_order_count + store_message_count
    return {
        'store_message_count': store_message_count,
        'user_message_count': user_message_count,
        'awaiting_order_count': awaiting_order_count,
        'store_activity_count': store_activity_count
        }
