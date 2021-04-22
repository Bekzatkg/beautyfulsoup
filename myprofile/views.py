from rest_framework import generics
from .models import ProfileMaster, ProfileCustomer
from .serializers import ProfileMasterSerializer, ProfileCustomerSerializer


class ProfileMasterListView(generics.ListAPIView):
    queryset = ProfileMaster.objects.all()
    serializer_class = ProfileMasterSerializer


class ProfileMasterDetailView(generics.RetrieveAPIView):
    queryset = ProfileMaster.objects.all()
    serializer_class = ProfileMasterSerializer


class ProfileMasterUpdateView(generics.UpdateAPIView):
    queryset = ProfileMaster.objects.all()
    serializer_class = ProfileMasterSerializer


class ProfileCustomerListView(generics.ListAPIView):
    queryset = ProfileCustomer.objects.all()
    serializer_class = ProfileCustomerSerializer


class ProfileCustomerDetailView(generics.RetrieveAPIView):
    queryset = ProfileCustomer.objects.all()
    serializer_class = ProfileCustomerSerializer


class ProfileCustomerUpdateView(generics.UpdateAPIView):
    queryset = ProfileCustomer.objects.all()
    serializer_class = ProfileCustomerSerializer
