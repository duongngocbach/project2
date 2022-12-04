import random
from .models import Content


def createRecord(number):
    for i in range(0, number):
        a = random.randint(1, 10000)
        b = random.randint(1, 50)
        Content.objects.create(total_mac=a, number_of_pop_tail=b)

def CreateIpRandom():
    list_content = Content.objects.all()
    for item in list_content:
        a = random.randint(1, 255)
        b = random.randint(1, 255)
        c = random.randint(1, 255)
        d = random.randint(1, 255)
        item.ip = str(a)+"."+str(b)+"."+str(c)+"."+str(d)
        item.save()


