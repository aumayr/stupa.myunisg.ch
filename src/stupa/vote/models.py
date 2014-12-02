from django.db import models
from django.contrib.auth.models import User


class Session(models.Model):
    name = models.CharField(max_length=128, unique=True)
    started_at = models.DateTimeField()

    def __unicode__(self):
        return self.name


class Question(models.Model):
    TYPE_OF_QUESTION = (
        ('OPEN', 'Open question'),
        ('ANON', 'Anonymous question')
    )

    session = models.ForeignKey(Session)
    text = models.TextField()
    time_opened = models.DateTimeField(blank=True, null=True)
    time_closed = models.DateTimeField(blank=True, null=True)
    number_of_voters = models.IntegerField(default=0)
    type_of_question = models.CharField(max_length=4,
                                        choices=TYPE_OF_QUESTION)
    ordering = models.IntegerField(default=1)

    class Meta:
        ordering = ['-ordering']

    # TODO def is_open(self)  => time_opened set, time_closed not set
    # TODO def result(self)   => tuple of (YES, NO, ABST)
    # TODO def valid_result() => checks if the count of answers is equal to
    #                            number_of_voters

    def __unicode__(self):
        return self.text


class Hashcode(models.Model):
    created_at = models.DateTimeField()
    session = models.ForeignKey(Session)
    code = models.CharField(max_length=9)
    user = models.ForeignKey(User, blank=True)

    # TODO def was_used(self) => checks if there is an answer containing
    #                            this hashcode


class Answer(models.Model):
    TYPE_OF_ANSWER = (
        ('YES', 'Yes'),
        ('NO', 'No'),
        ('ABST', 'abstention'),
    )

    hashcode = models.ForeignKey(Hashcode)
    choice = models.CharField(max_length=4,
                             choices=TYPE_OF_ANSWER)
