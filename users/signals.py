from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user = instance)

		sender_email = os.getenv('SENDER_EMAIL')
		message = Mail(
			from_email=sender_email,
			to_emails=str(instance.email),
			subject=f'Welcome Dear { instance.username }',
			html_content=f'<strong><em>Thank you for choosing MatriNome!</em></strong></p>')
		try:
			sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
			response = sg.send(message)
			print(response.status_code)
			print(response.body)
			print(response.headers)	
		except Exception as e:
			print(e.message)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	instance.profile.save()

