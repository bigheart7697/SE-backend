from django.shortcuts import get_object_or_404
from rest_framework import generics

from .permissions import IsStudent, IsAdviser
from .serializers import ConsultationRequestSerializer, ConsultationRequestResponseSerializer
from rest_framework.permissions import IsAuthenticated


class ConsultationRequestViewSet(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = ConsultationRequestSerializer

    def perform_create(self, serializer):
        serializer.save(
            student=self.request.user.student,
            adviser_id=self.kwargs.get('adviser')
        )


class ConsultationIncomingRequestsViewSet(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdviser]
    serializer_class = ConsultationRequestSerializer

    def get_queryset(self):
        return self.request.user.advisor.requests.all()


class ConsultationOutgoingRequestsViewSet(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = ConsultationRequestSerializer

    def get_queryset(self):
        return self.request.user.student.requests.all()


class ConsultationRequestResponseViewSet(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdviser]
    serializer_class = ConsultationRequestResponseSerializer

    def get_object(self):
        return get_object_or_404(self.request.user.advisor.requests, status='0', id=self.kwargs.get('request_id'))
