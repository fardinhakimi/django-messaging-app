from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import (Conversation, Message, Join)
from django.views.generic.list import ListView
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist


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

    def return_message(self, conversation, message, sender, recipient):
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

                             }, status=200)

    def post(self, request):
        recipient = User.objects.get(pk=int(request.POST.get('recipient_id')))
        sender = request.user
        conversation = Conversation.objects.get(pk=int(request.POST.get('conversation_id')))
        value = request.POST.get('message')

        message = Message.create_message(value, sender, recipient, conversation)

        if message is not None:
            return self.return_message(conversation, message, sender, recipient)
        else:
            return JsonResponse({"details": "bad request"}, status=400)



class ConversationView(View):

    def return_conversation_messages(self, request, other_user, conversation):
        messages = serializers.serialize('json', conversation.messages.all())

        return JsonResponse({"conversation_id": conversation.pk,
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

                             }, status=200
                            )

    def get(self, request):
        other_user = User.objects.get(pk=int(request.GET.get('user_id')))
        user = request.user

        conversation = Conversation.get_or_create_conversation(user, other_user)

        if conversation is not None:
            # read unread messages
            conversation.read_messages(user)

            # send conversation messages
            return self.return_conversation_messages(request, other_user, conversation)
        else:
            return JsonResponse({"details": "bad request"}, status=400)