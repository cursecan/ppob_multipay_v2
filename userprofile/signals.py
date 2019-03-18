from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from core.tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import send_mail

from .models import (
    Profile, Wallet, UploadUser
)


@receiver(post_save, sender=User)
def initial_user_profile(sender, instance, created, **kwargs):
    if created:
        profile_obj = Profile.objects.create(
            user = instance, 
            agen = instance
        )

        Wallet.objects.create(
            profile = profile_obj
        )

        # Sending Email
        subject = 'Warungid Account Activation'
        message = render_to_string('core/account_activation_email.html', {
            'user': instance,
            'domain': 'http://www.warungid.com',
            'uid': urlsafe_base64_encode(force_bytes(instance.pk)).decode(),
            'token': account_activation_token.make_token(instance),
        })
        send_mail(subject, message, 'no-reply@warungid.com', [instance.email])


@receiver(post_save, sender=UploadUser)
def add_bulk_user(sender, instance, created, **kwargs):
    if created:
        User.objects.create_user(
            username = instance.username,
            email = instance.username,
            password= instance.password,
            first_name = instance.first_name,
            last_name = instance.last_name
        )