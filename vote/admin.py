from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from .models import Session, Question, Hashcode, Answer

admin.site.site_header = "Studentenparlament Administration"

admin.site.register(Session)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('session', 'text', 'time_opened', 'is_open', 'type_of_question')
    list_filter = ('session', 'type_of_question')
    search_fields = ('text',)

admin.site.register(Question, QuestionAdmin)


class HashcodeAdmin(admin.ModelAdmin):
    list_display = ('session', 'code', 'user', 'is_active', 'created_at')
    list_filter = ('session', 'user', 'is_active')
    search_fields = ('session', 'user')
    ordering = ('created_at',)

admin.site.register(Hashcode, HashcodeAdmin)

def generate_hashcodes(modeladmin, request, queryset):
    return redirect('hashcodes_form')

generate_hashcodes.short_description = "Generate new hashcodes"


class StupaUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    actions = [generate_hashcodes]

admin.site.unregister(User)
admin.site.register(User, StupaUserAdmin)
