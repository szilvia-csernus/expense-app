from rest_framework import serializers
from .models import Church, CostPurpose


class CostPurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostPurpose
        fields = ['name', 'cost_code']


class ChurchDetailsSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    logo = serializers.ImageField()
    cost_purposes = CostPurposeSerializer(many=True, read_only=True)

    class Meta:
        model = Church
        fields = ['name', 'logo', 'cost_purposes']


class ChurchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Church
        fields = ['name']


class ChurchListSerializer(serializers.ModelSerializer):
    churches = ChurchSerializer(many=True, read_only=True)

    class Meta:
        model = Church
        fields = ['churches', 'name']
