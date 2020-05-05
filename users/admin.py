from django.contrib import admin
from .models import Profile, InterestChoice, User

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(InterestChoice)