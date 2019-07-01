from background_task import background
from django.core.mail import send_mail
from .models import BillingRecord
from django.template.loader import render_to_string

@background(schedule=1)
def sending_email_notif(bil_id):
    bil_obj = BillingRecord.objects.get(pk=bil_id)

    if bil_obj.payment:
        msg = render_to_string(
            'billing/income_email_notif.html',
            {'bil': bil_obj}
        )
        subject = 'Payment'

    if bil_obj.transfer:
        msg = render_to_string(
            'billing/transfer_email_notif.html',
            {'bil': bil_obj}
        )
        subject = 'Transfer'
        
    send_mail(subject, msg, 'info@warungid.com', [bil_obj.user.email])