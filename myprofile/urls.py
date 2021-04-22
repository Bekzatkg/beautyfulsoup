from django.urls import path
from .views import *

urlpatterns = [
    path('designer/', ProfileMasterListView.as_view()),
    path('designer/<int:pk>/', ProfileMasterDetailView.as_view()),
    path('designer-update/<int:pk>/', ProfileMasterUpdateView.as_view()),
    path('customer/', ProfileCustomerListView.as_view()),
    path('customer/<int:pk>/', ProfileCustomerDetailView.as_view()),
    path('customer-update/<int:pk>/', ProfileCustomerUpdateView.as_view()),
]
