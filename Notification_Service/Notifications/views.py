from django.shortcuts import render
from .models import Distribution, Customer, Message
from .serializers import MessageSerializer, CustomerSerializer, DistributionSerializer
from rest_framework import generics, views, response
from rest_framework.generics import GenericAPIView


class MessageApiView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class CustomerApiView(GenericAPIView):
    serializer_class = CustomerSerializer
    def get(self, request):
        lst = Customer.objects.all()
        return response.Response({'customers': CustomerSerializer(lst, many=True).data})

    def post(self, request):
        serializer = CustomerSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({'customers': serializer.data})

    def put(self, request, *args, **kwargs):
        customer_id = kwargs.get('id')
        try:
            instance = Customer.objects.get(pk=customer_id)
        except:
            return response.Response({'error': 'Object does not exist'})

        serializer = CustomerSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({'customers': serializer.data})

    def delete(self, request, *args, **kwargs):
        customer_id = kwargs.get('id')
        try:
            instance = Customer.objects.get(pk=customer_id)
        except:
            return response.Response({'error': 'Object does not exist'})
        instance.delete()
        return response.Response({'customers': str(customer_id) + ' deleted'})


class DistributionApiView(GenericAPIView):
    serializer_class = DistributionSerializer
    def get(self, request):
        lst = Distribution.objects.all()
        return response.Response({'distributions': DistributionSerializer(lst, many=True).data})

    def post(self, request):
        serializer = DistributionSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({'distributions': serializer.data})

    def put(self, request, *args, **kwargs):
        distribution_id = kwargs.get('id')
        try:
            instance = Distribution.objects.get(pk=distribution_id)
        except:
            return response.Response({'error': 'Object does not exist'})

        serializer = DistributionSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({'distributions': serializer.data})

    def delete(self, request, *args, **kwargs):
        distribution_id = kwargs.get('id')
        try:
            instance = Distribution.objects.get(pk=distribution_id)
        except:
            return response.Response({'error': 'Object does not exist'})
        instance.delete()
        return response.Response({'distributions': str(distribution_id) + ' deleted'})


def distributions_table(request):
    distributions = Distribution.objects.all()
    return render(request, 'Notifications/Distributions.html', {'distributions': distributions})


def customers_table(request):
    customers = Customer.objects.all()
    return render(request, 'Notifications/Customers.html', {'customers': customers})


def messages_table(request):
    messages = Message.objects.all()
    return render(request, 'Notifications/Messages.html', {'messages': messages})




