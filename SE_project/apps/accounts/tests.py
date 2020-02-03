from SE_project.utils import AbstractTest
from django.urls import reverse
from rest_framework import status

from .models import CustomUser


class TestAccount(AbstractTest):
    def test_student_edit_unauthenticated(self):
        data = {"name": "hoda"}
        response = self.client.post(reverse('student edit profile'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_student_edit(self):
        data = {"name": "mahooly"}
        token = self.client_login('mahooly', 'test1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.put(reverse('student edit profile'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        student = CustomUser.objects.get(username='mahooly').student
        self.assertEqual(student.name, 'mahooly')

    def test_adviser_edit_unauthenticated(self):
        data = {"name": "mahtab"}
        response = self.client.post(reverse('advisor edit profile'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_adviser_edit(self):
        data = {"education": "4"}
        token = self.client_login('hodhod', 'test1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.put(reverse('advisor edit profile'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        adviser = CustomUser.objects.get(username='hodhod').advisor
        self.assertEqual(adviser.education, '4')

    def test_adviser_search_name(self):
        data = {"name": "hod"}
        response = self.client.get(reverse('advisor list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        container = self.get_json_container(response)
        self.assertEqual(1, len(container))

    def test_adviser_search_age(self):
        data = {"min_age": "25"}
        response = self.client.get(reverse('advisor list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        container = self.get_json_container(response)
        self.assertEqual(1, len(container))

        data = {"max_age": "22"}
        response = self.client.get(reverse('advisor list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        container = self.get_json_container(response)
        self.assertEqual(0, len(container))

    def test_adviser_search_city(self):
        data = {"city": "Tehran"}
        response = self.client.get(reverse('advisor list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        container = self.get_json_container(response)
        self.assertEqual(2, len(container))

        data = {"name": "hod", "city": "Tehran"}
        response = self.client.get(reverse('advisor list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        container = self.get_json_container(response)
        self.assertEqual(1, len(container))

    def test_adviser_search_gender(self):
        data = {"name": "hod", "gender": "1"}
        response = self.client.get(reverse('advisor list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        container = self.get_json_container(response)
        self.assertEqual(0, len(container))
