import json
import re

from django.test import TestCase, Client

from apps.accounts.serializers import UserSerializer
from apps.accounts.models import CustomUser, Student, Field, Advisor
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


def custom_jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }


MOBILE_HTTP_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 ' \
                         'like Mac OS X) AppleWebKit/534.46' \
                         ' (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3'

DESKTOP_HTTP_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8)' \
                          ' AppleWebKit/537.13+' \
                          ' (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'


class AbstractTest(APITestCase):
    def setUp(self):
        self.populate_db()

    def populate_db(self):
        self.field1 = Field.objects.create(name="AI")
        self.field2 = Field.objects.create(name="Chemistry")
        self.field3 = Field.objects.create(name="Robotics")
        self.field4 = Field.objects.create(name="Computational Geometry")

        self.create_students()
        self.create_advisers()

    def create_students(self):
        student1_data = {"user": {"username": "mahooly", "email": "mahtab@gmail.com", "password": "test1234"},
                         "name": "mahtab", "age": 16, "gender": "2", "country": "Iran", "city": "Tehran",
                         "phone_number": "+989192162013", "grade": "3"}
        response = self.client.post(reverse('student register'), data=student1_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        container_json = self.get_json_container(response)
        self.student1 = Student.objects.get(name=container_json['name'])
        self.student1.fields_of_interest.set([self.field1, self.field3])

        student2_data = {"user": {"username": "bigheart", "email": "reza@gmail.com", "password": "test1234"},
                         "name": "reza", "age": 17, "gender": "1", "country": "Iran", "city": "Zanjan",
                         "phone_number": "+989123456678", "grade": "3"}
        response = self.client.post(reverse('student register'), data=student2_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        container_json = self.get_json_container(response)
        self.student2 = Student.objects.get(name=container_json['name'])
        self.student2.fields_of_interest.set([self.field1, self.field4])

    def create_advisers(self):
        adviser1_data = {"user": {"username": "hodhod", "email": "hoda@gmail.com", "password": "test1234"},
                         "name": "hoda", "age": 23, "gender": "2", "country": "Iran", "city": "Tehran",
                         "phone_number": "+989191234567", "education": "2"}
        response = self.client.post(reverse('advisor register'), data=adviser1_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        container_json = self.get_json_container(response)
        self.adviser1 = Advisor.objects.get(name=container_json['name'])

        adviser2_data = {"user": {"username": "morsal", "email": "parsa@gmail.com", "password": "test1234"},
                         "name": "parsa", "age": 27, "gender": "1", "country": "Iran", "city": "Tehran",
                         "phone_number": "+989192345678", "education": "2"}
        response = self.client.post(reverse('advisor register'), data=adviser2_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        container_json = self.get_json_container(response)
        self.adviser2 = Advisor.objects.get(name=container_json['name'])

    def client_login(self, username, password):
        data = {'username': username, 'password': password}
        response = self.client.post(reverse("token-auth"),
                                    data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        container_json = self.get_json_container(response)
        token = container_json['token']
        return token

    def get_json_container(self, response):
        response_dict = response.__dict__
        container = response_dict['_container'][0]
        container = container.decode("utf-8")
        container_json = json.loads(container)
        return container_json
