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
