from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext as _
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator


profile_images_dir = 'static/users/'


def age_choices():
    return [(r, r) for r in range(7, 100)]


class Gender(models.TextChoices):
    DEFAULT = '0', _('Default')
    MALE = '1', _('Male')
    FEMALE = '2', _('Female')


class Education(models.TextChoices):
    DEFAULT = '0', _('Default')
    DIPLOMA = '1', _('Diploma')
    BACHELOR = '2', _('Bachelor')
    MASTER = '3', _('Master')
    PHD = '4', _('P.hD.')


class Grade(models.TextChoices):
    DEFAULT = '0', _('Default')
    ELEMENTARY_SCHOOL = '1', _('Elementary School')
    PRE_HIGH_SCHOOL = '2', _('Pre-High School')
    HIGH_SCHOOL = '3', _('High School')


class CustomUser(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=200)
    last_name = models.CharField(_('last name'), max_length=200)
    gender = models.CharField(_('gender'), choices=Gender.choices, default=Gender.DEFAULT, max_length=200)
    age = models.IntegerField(_('age'), choices=age_choices(), default=18,
                              validators=[MaxValueValidator(100)])
    country = models.CharField(_('country'), max_length=100, null=True, blank=True)
    city = models.CharField(_('city'), max_length=100, null=True, blank=True)
    address = models.CharField(_('address'), max_length=100, null=True, blank=True)
    phone_number = PhoneNumberField(_('phone number'), unique=True, null=True, blank=True)
    photo = models.ImageField(_('photo'), upload_to=profile_images_dir, null=True, blank=True)
    is_advisor = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.username)


class Advisor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, unique=True)
    education = models.CharField(_('education'), max_length=200, choices=Education.choices)
    record = models.TextField(_('record'), null=True, blank=True)


class Field(models.Model):
    name = models.CharField(_('name'), max_length=200, primary_key=True, unique=True)


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, unique=True)
    grade = models.CharField(_('grade'), max_length=200, choices=Grade.choices)
    school_name = models.CharField(_('school name'), max_length=200, null=True, blank=True)
    last_grade_score = models.FloatField(_('last grade score'), null=True, blank=True, validators=[MaxValueValidator(20.0)])
    average_grade_score = models.FloatField(_('average grade score'), null=True, blank=True, validators=[MaxValueValidator(20.0)])
    fields_of_interest = models.ManyToManyField(Field, blank=True)