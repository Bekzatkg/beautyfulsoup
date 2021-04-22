from rest_framework import serializers
from .models import *


class ProfileMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileMaster
        fields = '__all__'


class ProfileCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileCustomer
        fields = '__all__'

