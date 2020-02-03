from rest_framework import permissions, filters
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Advisor, Student, Field
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import AdvisorEditSerializer, StudentSerializer, StudentEditSerializer, AdvisorSerializer, \
    FieldSerializer, AdvisorPublicSerializer


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


class AdvisorsListView(ListCreateAPIView):
    serializer_class = AdvisorPublicSerializer

    # permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = Advisor.objects.all()

        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        min_age = self.request.query_params.get('min_age')
        if min_age is not None:
            queryset = queryset.filter(age__gte=int(min_age))

        max_age = self.request.query_params.get('max_age')
        if max_age is not None:
            queryset = queryset.filter(age__lte=int(max_age))

        city = self.request.query_params.get('city')
        if city is not None:
            queryset = queryset.filter(city__icontains=city)

        gender = self.request.query_params.get('gender')
        if gender is not None:
            if gender == "1" or gender == "2":
                queryset = queryset.filter(gender=gender)

        return queryset.distinct()
