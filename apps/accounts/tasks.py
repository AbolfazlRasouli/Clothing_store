from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(bind=True)
def send_otp_by_email(self, email, otp):
    mail_subject = " Center OTP"
    message = \
        "Welcome!\n" \
        f"OTP Code: {otp}"
    
    to_email = email
    
    status = send_mail(
        subject= mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=False,
    )
    
    return status
