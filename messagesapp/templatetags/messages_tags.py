from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from messagesapp.models import (Message, Conversation)

register = template.Library()


@register.simple_tag
def get_stats(user_id):
    user = User.objects.get(pk=user_id)

    sent_messages_count= Message.objects.filter(owner=user).count()
    received_messages_count = Message.objects.filter(recipient=user).count()

    return {
        "sent_messages": sent_messages_count,
        "conversations": user.conversations.all().count(),
        "received_messages": received_messages_count
    }


@register.simple_tag
def get_unread_messages(sender_id, user_id):
    sender = User.objects.get(pk=sender_id)
    recipient = User.objects.get(pk=user_id)

    unread_messages_count = Message.objects.filter(owner=sender, recipient =recipient, read=False).count()

    return unread_messages_count


