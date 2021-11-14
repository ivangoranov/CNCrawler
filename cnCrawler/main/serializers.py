from rest_framework import serializers

from .models import ContractNotice
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")


class ContractNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractNotice
        fields = ['id', 'date', 'notice_number', 'tender_name', 'procedure_state', 'contract_type', 'type_of_procurement', 'estimated_value']

