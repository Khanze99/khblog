from __future__ import absolute_import, unicode_literals
import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError

logger = logging.getLogger('CELERY')


@shared_task
def send_to_mail_user(user, email):
    logger.info(f'send email user - {user} to email - {email}')
    try:
        send_mail(subject="Welcome {}! to blog".format(user), message=settings.EMAIL_MESSAGE.format(user=user),
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[email],
                  auth_user=settings.EMAIL_HOST_USER,
                  auth_password=settings.EMAIL_HOST_PASSWORD)
        logger.info('letter sent successfully')
    except BadHeaderError:
        logger.info('The letter was not sent, may be auth error on google smtp')


@shared_task
def send_mail_pass(user, email):
    logger.info(f'Password change notify user - {user} email - {email}')
    try:
        send_mail(subject="{}! Update your info".format(user), message='''You changed your information about you.
                        Respectfully''',
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[email],
                  auth_user=settings.EMAIL_HOST_USER,
                  auth_password=settings.EMAIL_HOST_PASSWORD)
        logger.info('letter sent successfully')
    except BadHeaderError:
        logger.info('The letter was not sent, may be auth error on google smtp')
