from django.test import TestCase
from messagesapp.models import Message, Conversation
from django.contrib.auth.models import User

class ConversationModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="fardin", password="test1234")
        self.other_user = User.objects.create(username="fardin2", password="test1234")
        self.conversation = Conversation.get_or_create_conversation(self.user, self.other_user)

    def test_conversation_creation(self):
        conversation = Conversation.get_or_create_conversation(self.user, self.other_user)
        #make sure we do not create another conversation for the same users
        reverse_conversation = Conversation.get_or_create_conversation(self.other_user, self.user)
        self.assertEquals("fardin-fardin2", conversation.name)
        self.assertEquals("fardin-fardin2", reverse_conversation.name)

    def test_conversation_exists(self):
        self.assertTrue(Conversation.conversation_exists(self.conversation.name))

    def test_conversation_does_not_exist(self):
        self.assertFalse(Conversation.conversation_exists("random_non_existent_name"))

    def test_conversation_members_count(self):

        print(self.conversation.get_conversation_members())
        self.assertEquals(2, self.conversation.get_conversation_members().count())



class MessageModelTest(TestCase):

    def setUp(self):

        self.sender = User.objects.create(username = "fardin", password = "test1234")
        self.recipient = User.objects.create(username="fardin2", password="test1234")
        self.conversation = Conversation.get_or_create_conversation(self.sender, self.recipient)

    def test_message_creation(self):
        value = "new message"
        message = Message.create_message(value, self.sender, self.recipient, self.conversation)

        self.assertEquals(value[:20], str(message))

    def test_message_unread(self):
        value = "new message"
        message = Message.create_message(value, self.sender, self.recipient, self.conversation)
        self.assertFalse(message.read)

    def test_message_read(self):
        value = "new message"
        message = Message.objects.create(value=value,
                                         owner=self.sender,
                                         recipient=self.recipient,
                                         conversation=self.conversation,
                                         read=True
                                         )
        self.assertTrue(message.read)

    def test_message_sender(self):

        value = "new message"
        message = Message.create_message(value, self.sender, self.recipient, self.conversation)
        self.assertEquals(self.sender, message.owner)

    def test_message_recipient(self):
        value = "new message"
        message = Message.create_message(value, self.sender, self.recipient, self.conversation)
        self.assertEquals(self.recipient, message.recipient)


