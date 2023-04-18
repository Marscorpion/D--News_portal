from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User

from .models import Category, Post

@shared_task
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]


        send_mail(
            subject=f'{Post.objects.get(pk=id).title}!',
            body=f'{Post.objects.get(pk=id).preview}',
            from_email='seafoamskl@yandex.ru',
            to=subscribers,
    )




