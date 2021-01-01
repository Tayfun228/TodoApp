from celery import shared_task
from django.core.mail import send_mail
from time import sleep


@shared_task
def set_expired_at(email,id,title):
    print(email)
    text=f'task {title} - Bitmesine son 10 deq'
    send_mail(
        'Subject here',
        text,
        'tccamalbyli@gmail.com',
        [email],
        fail_silently=False,
    )
    print("gozleme bitdi")
    return "gozleme bitdi"
