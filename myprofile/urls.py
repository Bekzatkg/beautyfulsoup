from django.urls import path
from .views import *

urlpatterns = [
    path('master/', ProfileMasterListView.as_view()),
    path('master/<int:pk>/', ProfileMasterDetailView.as_view()),
    path('master-update/<int:pk>/', ProfileMasterUpdateView.as_view()),
    path('customer/', ProfileCustomerListView.as_view()),
    path('customer/<int:pk>/', ProfileCustomerDetailView.as_view()),
    path('customer-update/<int:pk>/', ProfileCustomerUpdateView.as_view()),
]
