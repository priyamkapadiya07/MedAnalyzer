from django.contrib import admin

# Register your models here.
from .models import Report,UserProfile,UserQuestion

admin.site.register(Report)
admin.site.register(UserProfile)
admin.site.register(UserQuestion)