from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from PIL import Image
from django.core.validators import MinLengthValidator
from . import data


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


class InterestChoice(models.Model):
    interest = models.CharField(max_length=100, null=True) 

    def __str__(self):
        return self.interest


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    dob = models.DateField(null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    interests = models.ManyToManyField(InterestChoice)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)

    STATE_CHOICES = data.STATE_CHOICES
    state = models.IntegerField(choices=STATE_CHOICES, null=True)
    city = models.CharField(max_length=30)
    bio = models.TextField(max_length=150)
    address = models.TextField(max_length=100)
    mobile_no = models.CharField(max_length=10, validators=[MinLengthValidator(10)])
   
    
    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)