import random
import string
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from .models import User, Session, Hashcode

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
        new_hashcode = Hashcode(code=generate_random_string(), session=session, user=user)
        new_hashcode.save()
        user.set_password(new_hashcode.code)
        user.save()
        hashcodes_users[user] = new_hashcode


    hashcodes_anonymous = []
    for i in xrange(0, number_of_hashcodes):
        new_hashcode = Hashcode(code=generate_random_string(), session=session)
        new_hashcode.save()
        hashcodes_anonymous.append(new_hashcode)

    context_dict = { 'hashcodes_users': hashcodes_users, 'hashcodes_anonymous': hashcodes_anonymous }
    return render(request, 'hashcodes.html', context_dict)

def generate_random_string(length=8):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))
