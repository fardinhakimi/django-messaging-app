from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


# Create your models here.


class Conversation(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(User, through='Join')
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
    )

    def get_conversation_members(self):
        return self.members

    def read_messages(self, user):
        self.messages.filter(read=False, recipient=user, conversation=self).update(read=True)

    def unread_messages_count(self):
        return self.messages.filter(read=False).count()

    @classmethod
    def conversation_exists(cls, name):
        try:
            cls.objects.get(name=name)
            return True
        except ObjectDoesNotExist:
            return False

    @classmethod
    def get_or_create_conversation(cls, user, other_user):

        conversation_name = user.username + "-" + other_user.username
        revers_conversation_name = other_user.username + "-" + user.username

        if (cls.conversation_exists(conversation_name)):
            conversation = cls.objects.get(name=conversation_name)
        elif (cls.conversation_exists(revers_conversation_name)):
            conversation = cls.objects.get(name=revers_conversation_name)
        else:
            conversation = cls.objects.create(name=conversation_name)
            Join(user=user, conversation=conversation).save()
            Join(user=other_user, conversation=conversation).save()

        return conversation

    def __str__(self):

        return '%s' % (self.name)


class Join(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='conversations'
                             )
    conversation = models.ForeignKey(Conversation,
                                     on_delete=models.CASCADE,
                                     )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Join date',
    )

    def __str__(self):
        return str(self.pk)


class Message(models.Model):
    value = models.TextField(verbose_name='Value')

    owner = models.ForeignKey(
        User,
        related_name="sent_messages",
        on_delete=models.CASCADE
    )

    recipient = models.ForeignKey(
        User,
        related_name="received_messages",
        on_delete=models.DO_NOTHING
    )

    read = models.BooleanField(default=False)

    conversation = models.ForeignKey(
        'messagesapp.Conversation',
        verbose_name='Conversation',
        related_name='messages',
        on_delete=models.CASCADE
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
    )

    @classmethod
    def create_message(cls, value, sender, recipient, conversation):
        message = cls.objects.create(value=value,
                                     owner=sender,
                                     recipient=recipient,
                                     conversation=conversation
                                     )
        return message

    def __str__(self):
        return self.value[:20]
