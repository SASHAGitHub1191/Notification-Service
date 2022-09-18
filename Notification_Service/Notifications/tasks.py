import datetime
from Notification_Service.celery import app
import requests
from .models import Message
from Notification_Service import settings


@app.task
def message_sender(message_id, customer_phone_number, distribution_text, time):
    host = 'https://probe.fbrq.cloud/v1/send/' + str(message_id)
    expiration_time = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
    # Trying to send message until the server accepts it or the time runs out, and updating message status
    while datetime.datetime.now() < expiration_time:
        response = requests.post(host, headers={'accept': 'application/json', 'Authorization': 'Bearer ' + settings.JWT,
                                                'Content-type': 'application/json'}, json={
            'id': message_id,
            'phone': customer_phone_number,
            'text': distribution_text,
        })
        if response.text == '{"code":0,"message":"OK"}':
            message = Message.objects.get(pk=message_id)
            message.sended_status = 'Sended'
            message.save()
            return
        else:
            message = Message.objects.get(pk=message_id)
            message.sended_status = response.status_code
            message.save()
    return
