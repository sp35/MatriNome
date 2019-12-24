from django.db import models
from django.conf import settings
from django.utils import timezone


class RelationshipRequest(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_sent",
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_received",
    )

    message = models.TextField(blank=True)
    created = models.DateTimeField(default=timezone.now)
    rejected = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.from_user.username} to {self.to_user.username}"


class Partner(models.Model):
    its_partner = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="partner")
    current_user = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="user")
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.current_user.username} and {self.its_partner.username}"

    def save(self, *args, **kwargs):
        # Ensure users can't be friends with themselves
        if self.current_user == self.its_partner:
            raise ValidationError("Users cannot be related with themselves.")
        super(Partner, self).save(*args, **kwargs)