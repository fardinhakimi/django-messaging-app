from .models import ( Conversation , Message )
from django.core.exceptions import ObjectDoesNotExist

def does_conversation_exist(name):

    try:
        Conversation.objects.get(name=name)
        return True
    except ObjectDoesNotExist:
        return False

def get_conversation(name):
    return Conversation.objects.get(name=name)


def read_messages(sender, recipient):
    Message.objects.filter(owner=sender, recipient=recipient, read=False).update(read=True)
    return True