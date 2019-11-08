from django.db.models.signals import post_save
from django.dispatch import receiver
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from .models import RelationshipRequest, Partner


@receiver(post_save, sender=RelationshipRequest)
def req_sent(sender, instance, created, **kwargs):
	if created:
		sender_email = os.getenv('SENDER_EMAIL')
		message = Mail(
			from_email=sender_email,
			to_emails=str(instance.to_user.email),
			subject=f'Match Request from { instance.from_user.username }',
			html_content=f'<strong>{ instance.from_user.username } has sent you a match request. <br><em>Visit MatriNome to check if they are a perfect match for you.</em></strong></p>')
		try:
			sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
			response = sg.send(message)
			print(response.status_code)
			print(response.body)
			print(response.headers)	
		except Exception as e:
			print(e.message)


@receiver(post_save, sender=Partner)
def matched(sender, instance, created, **kwargs):
	if created:
		sender_email = os.getenv('SENDER_EMAIL')
		message = Mail(
			from_email=sender_email,
			to_emails=str(instance.current_user.email),
			subject=f"It's a Match",
			html_content=f"<strong>You and { instance.its_partner.username } are now Matched! <br><em> Hope we at MatriNome have successfully completed the job to connect you two.</em></strong>")
		try:
			sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
			response = sg.send(message)
			print(response.status_code)
			print(response.body)
			print(response.headers)	
		except Exception as e:
			print(e.message)