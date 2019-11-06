from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class InterestChoice(models.Model):
    INTEREST_CHOICES = (
        ('A', 'travelling'),
        ('B', 'exercise'),
        ('C', 'going to the theater'),
        ('D', 'dancing'),
        ('E', 'cooking'),
        ('F', 'doing stuff outdoors'),
        ('G', 'politics'),
        ('H', 'pets'),
        ('I', 'photography'),
        ('J', 'sports'),
        ('K', 'art'),
        ('L', 'learning'),
        ('M', 'music'),
        ('N', 'comedy'),
        ('O', 'reading'),
    )
    interest = models.CharField(max_length=1, choices=INTEREST_CHOICES, null=True) 

    def __str__(self):
        return self.get_interest_display()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    dob = models.DateField(null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    interests = models.ManyToManyField(InterestChoice)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)