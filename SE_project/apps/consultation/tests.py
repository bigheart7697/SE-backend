from SE_project.utils import AbstractTest
from django.urls import reverse
from rest_framework import status

from .models import ConsultationRequest


class TestConsultation(AbstractTest):
    def test_send_consultation_request_permissions(self):
        response = self.client.post(reverse('request consultation', kwargs={"adviser": self.adviser2.pk}), {},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        token = self.client_login('hodhod', 'test1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.post(reverse('request consultation', kwargs={"adviser": self.adviser2.pk}), {},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_send_consultation_request(self):
        token = self.client_login('mahooly', 'test1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.post(reverse('request consultation', kwargs={"adviser": self.adviser1.pk}), {},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        requests = ConsultationRequest.objects.all()
        self.assertEqual(1, requests.count())

    def test_view_sent_consultation_request_permissions(self):
        response = self.client.get(reverse('requests sent by student'), {},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        token = self.client_login('hodhod', 'test1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(reverse('requests sent by student'), {},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_accept_consultation_request(self):
        token = self.client_login('mahooly', 'test1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        self.client.post(reverse('request consultation', kwargs={"adviser": self.adviser1.pk}), {},
                         format='json')
        request = ConsultationRequest.objects.first()

        token = self.client_login('hodhod', 'test1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.put(
            reverse('send request response', kwargs={"request_id": request.id}), {"accepted": True},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        requests = ConsultationRequest.objects.filter(status='2')
        self.assertEqual(requests.count(), 1)

    def test_reject_consultation_request(self):
        token = self.client_login('mahooly', 'test1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        self.client.post(reverse('request consultation', kwargs={"adviser": self.adviser1.pk}), {},
                         format='json')
        request = ConsultationRequest.objects.first()

        token = self.client_login('hodhod', 'test1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.put(
            reverse('send request response', kwargs={"request_id": request.id}),
            {"accepted": False, "rejection_reason": "ugly person"},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        requests = ConsultationRequest.objects.filter(status='1')
        self.assertEqual(requests.count(), 1)

    def test_view_received_consultation_request_permissions(self):
        response = self.client.get(reverse('requests received by adviser'), {},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        token = self.client_login('mahooly', 'test1234')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(reverse('requests received by adviser'), {},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
