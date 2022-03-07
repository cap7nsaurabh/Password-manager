from django.contrib import admin
from account.models import cards,Entry,Meetings
# Register your models here.
admin.site.register(cards)
admin.site.register(Entry)
admin.site.register(Meetings)
