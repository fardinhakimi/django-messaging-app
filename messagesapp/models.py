from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Conversation(models.Model):

    name = models.CharField(max_length=128)
    members = models.ManyToManyField(User, through='Join')
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
    )

    def __str__(self):

        return '%s' % (self.name)


class Join(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name = 'conversations'
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
        on_delete= models.DO_NOTHING
     )

    read = models.BooleanField(default=False)

    conversation = models.ForeignKey(
        'messagesapp.Conversation',
        verbose_name= 'Conversation',
        related_name='messages',
        on_delete=models.CASCADE
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
    )

    def __str__(self):
        return self.value[:20]