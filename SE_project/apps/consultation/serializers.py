from django.db.transaction import atomic
from rest_framework import serializers

from .models import ConsultationRequest
from ..accounts.serializers import AdvisorSerializer, StudentSerializer


class ConsultationRequestSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    adviser = AdvisorSerializer(read_only=True)

    class Meta:
        model = ConsultationRequest
        fields = ('id', 'student', 'adviser', 'message', 'rejection_reason', 'status')
        read_only_fields = ('id', 'student', 'adviser', 'rejection_reason', 'status')


class ConsultationRequestResponseSerializer(serializers.ModelSerializer):
    accepted = serializers.BooleanField(write_only=True)

    class Meta:
        model = ConsultationRequest
        fields = ('accepted', 'rejection_reason')

    @atomic
    def update(self, instance, validated_data):
        accepted = validated_data.get('accepted', False)
        validated_data['status'] = '1' if accepted else '2'
        return super().update(instance, validated_data)
