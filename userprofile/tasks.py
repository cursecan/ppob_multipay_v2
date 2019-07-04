from background_task import background
from django.template.loader import render_to_string
from django.core.mail import send_mail

from .models import Profile

@background(schedule=1)
def send_email_invois():
    profile_objs = Profile.objects.filter(
        wallet__init_loan__gt=0
    )

    for i in profile_objs:
        msg = render_to_string(
            'userprofile/email_invois.html',
            {'name': i.get_fullname(), 'amount':i.wallet.get_loan()+i.wallet.init_loan}
        )
        subject = 'Informasi Tagihan Warungid'
        send_mail(subject, msg, 'info@warungid.com', [i.user.email])


