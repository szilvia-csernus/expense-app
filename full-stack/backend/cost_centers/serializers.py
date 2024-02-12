from rest_framework import serializers
from .models import Church, CostPurpose


class CostPurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostPurpose
        fields = ['name', 'cost_code']


class ChurchDetailsSerializer(serializers.ModelSerializer):
    short_name = serializers.CharField()
    long_name = serializers.CharField()
    logo = serializers.ImageField()
    cost_purposes = CostPurposeSerializer(many=True, read_only=True)
    claims_counter = serializers.IntegerField()
    finance_contact_name = serializers.CharField()
    finance_email = serializers.EmailField()

    class Meta:
        model = Church
        fields = ['short_name', 'long_name', 'logo',
                  'claims_counter', 'finance_contact_name',
                  'finance_email', 'cost_purposes']


class ChurchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Church
        fields = ['short_name']


class ChurchListSerializer(serializers.ModelSerializer):
    churches = ChurchSerializer(many=True, read_only=True)

    class Meta:
        model = Church
        fields = ['churches', 'short_name']
