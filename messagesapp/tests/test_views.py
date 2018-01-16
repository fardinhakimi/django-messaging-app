from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from messagesapp.models import Conversation

class UserListViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='fardin')
        self.user.set_password('test1234')
        self.user.save()
        self.client = Client()

    def test_list_view_users_with_login(self):
        # login the user
        self.client.login(username='fardin', password='test1234')
        response = self.client.get(reverse('users-list'))
        self.assertEqual(response.status_code, 200)
        # returns an array of users
        self.assertQuerysetEqual(response.context['users'], [])

    def test_list_view_users_without_login(self):
        response = self.client.get(reverse('users-list'))
        # redirects to login view
        self.assertEqual(response.status_code, 302)


class MessageViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='fardin')
        self.user.set_password('test1234')
        self.user.save()
        self.recipient = User.objects.create(username='zohra')
        self.recipient.set_password('test1234')
        self.recipient.save()
        self.conversation = Conversation.get_or_create_conversation(self.user, self.recipient)
        self.message = "hello there !"
        self.client = Client()

    def test_message_success(self):
        # login the user
        self.client.login(username='fardin', password='test1234')
        response = self.client.post(reverse('post-message'), {'recipient_id' : self.recipient.pk,
                                                              'message': self.message,
                                                              'conversation_id':self.conversation.pk })
        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(str(response.content, encoding='utf8'),{"conversation_id": self.conversation.pk,
                           "message": self.message,

                           "members": {

                               "sender": {
                                   "id": self.user.pk,
                                   "username": self.user.username
                               },

                               "recipient": {
                                   "id": self.recipient.pk,
                                   "username": self.recipient.username
                               }
                           }

                           })

    class ConversationViewTest(TestCase):
        def setUp(self):
            self.user = User.objects.create(username='fardin')
            self.user.set_password('test1234')
            self.user.save()
            self.other_user = User.objects.create(username='zohra')
            self.other_user.set_password('test1234')
            self.other_user.save()
            self.conversation = Conversation.get_or_create_conversation(self.user, self.other_user)
            self.message = "hello there !"
            self.client = Client()

        def test_conversation_success(self):
            # login the user
            self.client.login(username='fardin', password='test1234')
            response = self.client.get(reverse('get-messages'), {'user_id': self.recipient.pk})
            self.assertEqual(response.status_code, 200)
            # returns an array of users
            self.assertJSONEqual(str(response.content, encoding='utf8'), {"conversation_id": self.conversation.pk,
                                                                          "messages": [],

                                                                          "members": {

                                                                              "sender": {
                                                                                  "id": self.user.pk,
                                                                                  "username": self.user.username
                                                                              },

                                                                              "recipient": {
                                                                                  "id": self.other_user.pk,
                                                                                  "username": self.other_user.username
                                                                              }
                                                                          }

                                                                          })



