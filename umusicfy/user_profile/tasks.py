from celery import shared_task
from django.template import loader
from django.conf import settings
from django.core.mail import send_mail

EMAIL_TEMPLATE_NAME = 'playlist_notification.txt'
EMAIL_SUBJECT_TEMPLATE_NAME = 'playlist_notification_subject.txt'


@shared_task
def send_email_notification_task(user, playlist):
    context = {
        'user': user,
        'playlist': playlist,
    }
    body = loader.render_to_string(EMAIL_TEMPLATE_NAME,
                                   context).strip()
    subject = loader.render_to_string(EMAIL_SUBJECT_TEMPLATE_NAME,
                                      context).strip()
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
              [user.email])
    return 'The notification for new playlist has been send to user "%s" ' % user.username
