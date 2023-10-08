import sys
import os
import subprocess

if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pika
from mongoengine import connect
from models import Contact
from uploads import user, passwd, domain, db_name

connect(host=f"mongodb+srv://{user}:{passwd}@{domain}/{db_name}")

def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects.get(id=contact_id)
    send_email(contact.email)
    contact.message_sent = True
    contact.save()


def send_email(email):
    print(f"Sending email to {email}")


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="email_queue")

channel.basic_consume(queue="email_queue", on_message_callback=callback, auto_ack=True)

print("Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
