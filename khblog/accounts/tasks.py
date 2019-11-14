from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_to_mail_user(user, email):
    send_mail(subject="Welcome {}! to blog".format(user), message=settings.EMAIL_MESSAGE,
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=[email],
              auth_user=settings.EMAIL_HOST_USER,
              auth_password=settings.EMAIL_HOST_PASSWORD)


@shared_task
def send_mail_pass(user, email):
    send_mail(subject="{}! Update your info".format(user), message='''You changed your information about you.
                    Respectfully''',
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=[email],
              auth_user=settings.EMAIL_HOST_USER,
              auth_password=settings.EMAIL_HOST_PASSWORD)