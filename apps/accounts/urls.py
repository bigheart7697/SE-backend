from django.conf.urls import url
from django.urls import include
from rest_framework_jwt.views import obtain_jwt_token

from .views import ProfileDetailView, AdvisorCreateView, StudentCreateView, StudentUpdateView, AdvisorUpdateView, \
    AdvisorsListView

urlpatterns = [
    url(r'^login/', obtain_jwt_token, name='token-auth'),
    url(r'^advisor-register/', AdvisorCreateView.as_view(), name="advisor register"),
    url(r'^student-register/', StudentCreateView.as_view(), name="student register"),
    url(r'^student-edit-profile/', StudentUpdateView.as_view(), name="student edit profile"),
    url(r'^advisor-edit-profile/$', AdvisorUpdateView.as_view(), name="advisor edit profile"),
    url(r'^user/$', ProfileDetailView.as_view(), name="profile"),
    url(r'^advisors-list/$', AdvisorsListView.as_view(), name="advisor list")
]
