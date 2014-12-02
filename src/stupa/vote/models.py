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

    def is_open(self):
        return self.time_opened and not self.time_closed
    is_open.boolean = True  # for Django Admin

    def number_of_votes_cast(self):
        return Answer.objects.filter(question=self).count()

    def result(self):
        return {
            'yes':  Answer.objects.filter(question=self, choice='YES').count(),
            'no':   Answer.objects.filter(question=self, choice='NO').count(),
            'abst': Answer.objects.filter(question=self, choice='ABST').count()
        }

    def result_string(self):
        result = self.result()
        number_of_votes_cast = self.number_of_votes_cast()
        return "%s (%s Ja, %s Nein, %s Enthaltung)" % (number_of_votes_cast, result['yes'], result['no'], result['abst'])

    def valid_result(self):
        return self.number_of_voters == self.number_of_votes_cast

    def __unicode__(self):
        return self.text


class Hashcode(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(Session)
    is_active = models.BooleanField(default=True)
    code = models.CharField(max_length=9)
    user = models.ForeignKey(User, blank=True, null=True)

    # TODO def was_used(self) => checks if there is an answer containing
    #                            this hashcode

    def __unicode__(self):
        return "%s: %s (%s)" % (self.session, self.code, self.user)

class Answer(models.Model):
    TYPE_OF_ANSWER = (
        ('YES', 'Yes'),
        ('NO', 'No'),
        ('ABST', 'abstention'),
    )

    question = models.ForeignKey(Question)
    hashcode = models.ForeignKey(Hashcode)
    choice = models.CharField(max_length=4,
                             choices=TYPE_OF_ANSWER)

    def __unicode__(self):
        return "Answer (%s, %s)" % (self.question.text, self.hashcode)
