from django.contrib import admin
from .models import Session, Question, Hashcode, Answer

admin.site.register(Session)
admin.site.register(Question)
admin.site.register(Hashcode)
admin.site.register(Answer)
