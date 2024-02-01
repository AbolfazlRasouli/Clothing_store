from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone


@shared_task(bind=True)
def send_otp_by_email(self, email, otp):
    mail_subject = " Center OTP"
    message = \
        "Welcome!\n" \
        f"OTP Code: {otp}"
    
    to_email = email
    
    status = send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=False,
    )
    
    return status


@shared_task(bind=True)
def verify_link(self, email, link):
    mail_subject = " verify link "
    message = \
        "clik on this link!\n" \
        f"link: http://127.0.0.1:8000{link}"

    to_email = email

    status = send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=False,
    )

    return status


@shared_task
def delete_user():
    users = get_user_model().objects.filter(is_active=False)
    time_now = timezone.now()
    for user in users:
        date_joined = user.date_joined
        distance_time = time_now - date_joined
        if distance_time >= timezone.timedelta(seconds=60):
            user.hard_delete()


@shared_task(bind=True)
def send_by_email(self, email, link):
    mail_subject = " Password Reset"
    message = \
        "clik on this link!\n" \
        f"link: http://127.0.0.1:8000/{link}"

    to_email = email

    status = send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=False,
    )

    return status