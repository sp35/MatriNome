from django.contrib import admin
from .models import Profile, InterestChoice, CustomUser

admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(InterestChoice)