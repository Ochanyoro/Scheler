from django.contrib import admin

# Register your models here.
from .models import Schedule,Friend,Group,Good

admin.site.register(Schedule)
admin.site.register(Friend)
admin.site.register(Group)
admin.site.register(Good)
