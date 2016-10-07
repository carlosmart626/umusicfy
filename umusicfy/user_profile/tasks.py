from celery import shared_task
from django.template import loader
from django.conf import settings
from django.core.mail import send_mail

EMAIL_TEMPLATE_NAME = 'user_profile/playlist_notification.txt'
EMAIL_SUBJECT_TEMPLATE_NAME = 'user_profile/playlist_notification_subject.txt'


@shared_task
def send_email_notification_task(user_profile, playlist):
    context = {
        'user': user_profile,
        'playlist': playlist,
    }
    body = loader.render_to_string(EMAIL_TEMPLATE_NAME,
                                   context).strip()
    subject = loader.render_to_string(EMAIL_SUBJECT_TEMPLATE_NAME,
                                      context).strip()
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
              [user_profile.user.email])
    return 'The notification for new playlist has been send to user "%s" ' % user_profile.user.username
