from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Message, Customer, Distribution


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'sending_time', 'sended_status', 'distribution_id', 'customer_id')


class CustomerSerializer(serializers.Serializer):
    phoneNumberRegex = RegexValidator(regex=r"^7?1?\d{10,10}$")  # Checking phone number
    id = serializers.IntegerField(validators=[UniqueValidator(queryset=Customer.objects.all())])
    phone_number = serializers.CharField(validators=[phoneNumberRegex,
                                                     UniqueValidator(queryset=Customer.objects.all())],
                                         max_length=16)
    tag = serializers.CharField(max_length=255)
    timezone = serializers.IntegerField(default='0')

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.tag = validated_data.get('tag', instance.tag)
        instance.timezone = validated_data.get('timezone', instance.timezone)
        return instance

    class Meta:
        model = Customer
        fields = ('id', 'phone_number', 'operator_code', 'tag', 'timezone')

class DistributionSerializer(serializers.Serializer):
    id = serializers.IntegerField(validators=[UniqueValidator(queryset=Distribution.objects.all())])
    timer = serializers.DateTimeField()
    text = serializers.CharField()
    filter = serializers.CharField(max_length=255)
    timer_end = serializers.DateTimeField()

    def create(self, validated_data):
        return Distribution.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.timer = validated_data.get('timer', instance.timer)
        instance.text = validated_data.get('text', instance.text)
        instance.filter = validated_data.get('filter', instance.filter)
        instance.timer_end = validated_data.get('timer_end', instance.timer_end)
        return instance

    class Meta:
        model = Distribution
        fields = ('id', 'timer', 'text', 'filter', 'timer_end')
