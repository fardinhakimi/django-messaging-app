from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import (Conversation, Message, Join)
from django.views.generic.list import ListView
from django.core import serializers
from .helpers import (does_conversation_exist, get_conversation, read_messages)


class IndexView(View):
    def get(self, request):

        if request.user.is_authenticated:
            return redirect('users-list')
        else:
            return redirect('accounts:login')


class UserListView(ListView):
    template_name = "messagesapp/users.html"
    context_object_name = "users"

    def get_queryset(self):
        return User.objects.filter(is_superuser=False).exclude(username=self.request.user.username)


class MessageView(View):

    def post(self, request):
        recipient = User.objects.get(pk=int(request.POST.get('recipient_id')))
        sender = request.user
        conversation = Conversation.objects.get(pk=int(request.POST.get('conversation_id')))
        value = request.POST.get('message')

        message = Message.objects.create(value=value,
                                         owner=sender,
                                         recipient=recipient,
                                         conversation=conversation
                                         )
        message.save()

        return JsonResponse({"conversation_id": conversation.pk,
                             "message": message.value,

                             "members": {

                                 "sender": {
                                     "id": sender.pk,
                                     "username": sender.username
                                 },

                                 "recipient": {
                                     "id": recipient.pk,
                                     "username": recipient.username
                                 }
                             }

                             })


class ConversationView(View):

    def get(self, request):
        other_user = User.objects.get(pk=int(request.GET.get('user_id')))
        user = request.user
        conversation_name = user.username + "-" + other_user.username
        revers_conversation_name = other_user.username + "-" + user.username

        if (does_conversation_exist(conversation_name)):
            private_conversation = get_conversation(name=conversation_name)
        elif (does_conversation_exist(revers_conversation_name)):
            private_conversation = get_conversation(name=revers_conversation_name)
        else:
            private_conversation = Conversation.objects.create(name=conversation_name)
            Join(user=user, conversation=private_conversation).save()
            Join(user=other_user, conversation=private_conversation).save()

        messages = serializers.serialize('json', private_conversation.messages.all())
        # read unread messages
        read_messages(other_user, user)

        return JsonResponse({"conversation_id": private_conversation.pk,
                             "messages": messages,

                             "members": {

                                 "sender": {
                                     "id": request.user.pk,
                                     "username": request.user.username
                                 },

                                 "recipient": {
                                     "id": other_user.pk,
                                     "username": other_user.username
                                 }
                             }

                             })
