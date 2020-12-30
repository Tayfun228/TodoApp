from celery import shared_task
from time import sleep

@shared_task
def add():
    print('BASLADI')
    sleep(10)
    print("gozleme bitdi")
    return "gozleme bitdi"
