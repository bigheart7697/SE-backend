from django.db import models
from ..accounts.models import Student, Advisor
from django.utils.translation import ugettext as _


class Status(models.TextChoices):
    DEFAULT = '0', _('Pending')
    SENT = '1', _('Accepted')
    ACCEPTED = '2', _('Declined')


class ConsultationRequest(models.Model):
    student = models.ForeignKey(Student, related_name='requests', on_delete=models.PROTECT)
    adviser = models.ForeignKey(Advisor, related_name='requests', on_delete=models.PROTECT)
    message = models.TextField(blank=True, null=True)
    rejection_reason = models.TextField(null=True, blank=True)
    status = models.CharField(_('status'), choices=Status.choices, default=Status.DEFAULT, max_length=50)
