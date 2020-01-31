from django.conf.urls import url

from .views import ConsultationRequestViewSet, ConsultationOutgoingRequestsViewSet, ConsultationIncomingRequestsViewSet, \
    ConsultationRequestResponseViewSet

urlpatterns = [
    url(r'^request-consultation/(?P<adviser>\d+)/', ConsultationRequestViewSet.as_view(), name="request consultation"),
    url(r'^sent-requests/', ConsultationOutgoingRequestsViewSet.as_view(), name="requests sent by student"),
    url(r'^received-requests/', ConsultationIncomingRequestsViewSet.as_view(), name="requests received by adviser"),
    url(r'^send-request-response/(?P<request_id>\d+)/', ConsultationRequestResponseViewSet.as_view(),
        name="send request response"),
]
