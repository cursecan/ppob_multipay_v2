from background_task import background
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

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


@background(schedule=1)
def send_invois_email_api():
    profile_objs = Profile.objects.filter(
        wallet__init_loan__gt=0
    )
	for i in profile_objs:
		"https://api.mailgun.net/v3/mg.warungid.com/messages",
		auth=("api", settings.MG_KEY),
		data={"from": "Warungid Info <info@mg.warungid.com>",
			"to": "{} <{}}>".format(i.get_fullname(), i.user.email),
			"subject": "Informasi Tagihan Warungid",
			"template": "alertemplate",
			"h:X-Mailgun-Variables": json.dumps({"full_name": i.get_fullname(), "amount":"{:,.2f}".format(int(i.wallet.get_loan()+i.wallet.init_loan))})})