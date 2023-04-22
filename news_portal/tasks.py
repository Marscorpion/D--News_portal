from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from .models import Category, Post
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# @shared_task
# def notify_about_new_post_added(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         categories = instance.category.all()
#         subscribers: list[str] = []
#         for category in categories:
#             subscribers += category.subscribers.all()
#
#         subscribers = [s.email for s in subscribers]
#
#
#         send_mail(
#             subject=f'{Post.objects.get(pk=id).title}!',
#             body=f'{Post.objects.get(pk=id).preview}',
#             from_email='seafoamskl@yandex.ru',
#             to=subscribers,
#     )

@shared_task
def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body=preview,
        from_email='seafoamskl@yandex.ru',
        to=subscribers,
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send()

