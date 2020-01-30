from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from .models import Advisor, Student
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import AdvisorEditSerializer, StudentSerializer, StudentEditSerializer, AdvisorSerializer

class AdvisorCreateView(CreateAPIView):
    serializer_class = AdvisorSerializer


class AdvisorUpdateView(UpdateAPIView):
    queryset = Advisor.objects.all()
    serializer_class = AdvisorEditSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerProfileOrReadOnly]


class StudentCreateView(CreateAPIView):
    serializer_class = StudentSerializer


class StudentUpdateView(UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentEditSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerProfileOrReadOnly]


class ProfileDetailView(RetrieveAPIView):
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication, BasicAuthentication]

    def get_serializer_class(self):
        if self.request.user.is_Advisor:
            return AdvisorSerializer
        else:
            return StudentSerializer

    def get_queryset(self):
        if self.request.user.is_Advisor:
            return Advisor.objects.all()
        else:
            return Student.objects.all()
