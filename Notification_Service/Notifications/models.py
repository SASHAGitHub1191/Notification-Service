import datetime
from django.db import models
from django.core.validators import RegexValidator


class Distribution(models.Model):
    id = models.BigAutoField(primary_key=True)
    timer = models.DateTimeField()
    text = models.TextField()
    filter = models.CharField(max_length=64, blank=True)
    timer_end = models.DateTimeField()

    def __str__(self):
        return self.text[:80]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for i in Customer.objects.all():
            tag_list = i.tag.split(',')
            if self.filter == '':
                Message(sending_time=self.timer, distribution_id=self, customer_id=i).save_and_create_task()
                continue
            if self.filter in tag_list:
                Message(sending_time=self.timer, distribution_id=self, customer_id=i).save_and_create_task()
                continue
            if self.filter == i.operator_code:
                Message(sending_time=self.timer, distribution_id=self, customer_id=i).save_and_create_task()
                continue


class Customer(models.Model):
    phoneNumberRegex = RegexValidator(regex=r"^7?1?\d{10,10}$")
    id = models.BigAutoField(primary_key=True)
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True)
    operator_code = models.CharField(max_length=3, editable=False)
    tag = models.CharField(max_length=255)
    timezone = models.IntegerField(default='0')

    def __str__(self):
        return str(self.phone_number)

    def save(self, *args, **kwargs):
        self.operator_code = self.phone_number[1:4]
        super().save(*args, **kwargs)


class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    sending_time = models.DateTimeField()
    sended_status = models.CharField(max_length=255, default='Waiting')
    distribution_id = models.ForeignKey(Distribution, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # Saving created message and creating Celery task, that starts executing at a specific time
    def save_and_create_task(self, *args, **kwargs):
        from .tasks import message_sender
        super().save(*args, **kwargs)
        print(self.distribution_id.timer_end + datetime.timedelta(hours=self.customer_id.timezone))
        message_sender.apply_async(
            args=[self.id,
                  self.customer_id.phone_number,
                  self.distribution_id.text,
                  self.distribution_id.timer_end + datetime.timedelta(hours=self.customer_id.timezone)
                  ],
            eta=self.distribution_id.timer + datetime.timedelta(hours=self.customer_id.timezone),
        )
