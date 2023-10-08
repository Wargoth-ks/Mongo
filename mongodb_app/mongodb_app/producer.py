import sys
import os

if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pika
from mongoengine import connect
from faker import Faker
from models import Contact
from uploads import user, passwd, domain, db_name

connect(host=f"mongodb+srv://{user}:{passwd}@{domain}/{db_name}")

fake = Faker()

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="email_queue")

for _ in range(100):
    full_name = fake.name()
    email = fake.email()
    contact = Contact(full_name=full_name, email=email)
    contact.save()

    channel.basic_publish(exchange="", routing_key="email_queue", body=str(contact.id))

connection.close()
