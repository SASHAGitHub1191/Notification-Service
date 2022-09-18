from django.urls import path
from . import views
from .views import MessageApiView, CustomerApiView, DistributionApiView
from rest_framework import permissions
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Notification_Service API",
      default_version='v1',
      description="",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', views.distributions_table),
    path('customers', views.customers_table),
    path('messages', views.messages_table),
    path('api/v1/message_list/', MessageApiView.as_view()),
    path('api/v1/customer_list/', CustomerApiView.as_view()),
    path('api/v1/customer_list/<int:id>/', CustomerApiView.as_view()),
    path('api/v1/distribution_list/', DistributionApiView.as_view()),
    path('api/v1/distribution_list/<int:id>/', DistributionApiView.as_view()),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
