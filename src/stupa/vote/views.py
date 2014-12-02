import random
import string
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User, Session, Hashcode, Question, Answer

def index(request):
    context_dict = { 'message': "I am text from the context" }
    return render(request, 'index.html', context_dict)

@user_passes_test(lambda u: u.is_staff)
def hashcodes_form(request):
    sessions = Session.objects.all()
    user_ids = request.GET.getlist('ids', [])
    users = User.objects.filter(id__in=user_ids)
    context_dict = { 'sessions': sessions, 'users': users }
    return render(request, 'hashcodes_form.html', context_dict)

@user_passes_test(lambda u: u.is_staff)
def generate_hashcodes(request):
    session_id = int(request.POST.get('session_id', -1))
    session = Session.objects.get(id=session_id)
    number_of_hashcodes = int(request.POST.get('number_of_hashcodes', 50))
    user_ids = request.POST.getlist('user_id', [])
    users = User.objects.filter(id__in=user_ids)

    Hashcode.objects.all().update(is_active=False)

    hashcodes_users = {}   # user: hashcode
    for user in users:
        new_hashcode = Hashcode(code=_generate_random_string(), session=session, user=user)
        new_hashcode.save()
        user.set_password(new_hashcode.code)
        user.save()
        hashcodes_users[user] = new_hashcode


    hashcodes_anonymous = []
    for i in xrange(0, number_of_hashcodes):
        new_hashcode = Hashcode(code=_generate_random_string(), session=session)
        new_hashcode.save()
        hashcodes_anonymous.append(new_hashcode)

    context_dict = { 'hashcodes_users': hashcodes_users, 'hashcodes_anonymous': hashcodes_anonymous }
    return render(request, 'hashcodes.html', context_dict)

def _generate_random_string(length=8):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

def login(request):
    if request.POST:
        user_hashcode_str = request.POST.get('user_hashcode', '')
        anonymous_hashcode_str = request.POST.get('anonymous_hashcode', '')

        user_hashcode = None
        user_tmp = None
        anonymous_hashcode = None

        # TODO check if hashcode is active!

        try:
            user_hashcode = Hashcode.objects.get(code=user_hashcode_str)
            user_tmp = user_hashcode.user
            anonymous_hashcode = Hashcode.objects.get(code=anonymous_hashcode_str)
        except ObjectDoesNotExist, e:
            pass

        if not user_hashcode or not user_tmp or not anonymous_hashcode:
            messages.error(request, 'Hashcodes not found.')
        else:
            user = authenticate(username=user_tmp.username, password=user_hashcode.code)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    request.session['anonymous_hashcode'] = anonymous_hashcode.code
                    request.session['user_hashcode'] = user_hashcode.code
                    return redirect('question')
                else:
                    messages.error(request, 'Hashcodes not valid (Account disabled).')
            else:
                messages.error(request, 'Hashcodes not valid.')

    return render(request, 'login.html', {})

@login_required
def question(request):
    questions = Question.objects.filter(time_opened__isnull=False, time_closed__isnull=True)
    question = None
    has_voted = False

    if len(questions) > 0:
        has_voted = False
        question = questions[0]
        if question.type_of_question == 'OPEN':
            hashcode = Hashcode.objects.get(code=request.session['user_hashcode'])
        else:
            hashcode = Hashcode.objects.get(code=request.session['anonymous_hashcode'])

        # TODO check if hashcode is active!

        # see if there is an answer with this hashcode already
        answers = Answer.objects.filter(hashcode=hashcode)
        if answers.count() > 0:
            has_voted = True

    context_dict = { 'question': question, 'has_voted': has_voted }
    return render(request, 'question.html', context_dict)

@login_required
def vote(request):
    question_id = int(request.POST.get('question_id', -1))

    #try:
    question = Question.objects.get(time_opened__isnull=False, time_closed__isnull=True, id=question_id)
    if question.type_of_question == 'OPEN':
        hashcode = Hashcode.objects.get(code=request.session['user_hashcode'])
    else:
        hashcode = Hashcode.objects.get(code=request.session['anonymous_hashcode'])

    if len(Answer.objects.filter(hashcode=hashcode, question=question)) > 0:
        raise

    if question.number_of_votes_cast()+1 > question.number_of_voters:
        raise

    choice = request.POST.get('choice', 'None')
    if choice == 'None':
        raise

    answer = Answer(question=question, choice=choice, hashcode=hashcode)
    answer.save()
    return render(request, 'thanks_for_voting.html', {})

  #  except Exception, e:
  #      raise e

    return redirect('question')

@login_required
def results(request):
    sessions = Session.objects.all()
    return render(request, 'results.html', { 'sessions': sessions })
