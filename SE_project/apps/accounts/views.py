from rest_framework import permissions
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Advisor, Student, Field
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import AdvisorEditSerializer, StudentSerializer, StudentEditSerializer, AdvisorSerializer, \
    FieldSerializer


class AdvisorCreateView(CreateAPIView):
    serializer_class = AdvisorSerializer


class AdvisorUpdateView(UpdateAPIView):
    queryset = Advisor.objects.all()
    serializer_class = AdvisorEditSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerProfileOrReadOnly]

    def get_object(self):
        return self.request.user.advisor


class StudentCreateView(CreateAPIView):
    serializer_class = StudentSerializer


class StudentUpdateView(UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentEditSerializer
    permission_classes = [IsAuthenticated, IsOwnerProfileOrReadOnly]

    def get_object(self):
        return self.request.user.student


class ProfileDetailView(RetrieveAPIView):
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]
    # authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_serializer_class(self):
        if self.request.user.is_advisor:
            return AdvisorSerializer
        else:
            return StudentSerializer

    def get_object(self):
        if self.request.user.is_advisor:
            return self.request.user.advisor
        else:
            return self.request.user.student

    # def get_queryset(self):
    #     if self.request.user.is_advisor:
    #         return Advisor.objects.all()
    #     else:
    #         return Student.objects.all()


class AbilitiesViewSet(ListAPIView):
    serializer_class = FieldSerializer
    queryset = Field.objects.all()