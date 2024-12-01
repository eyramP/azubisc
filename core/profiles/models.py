from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from core.common.models import TimeStampedModel

User = get_user_model()

class Profile(TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = "Male", _('Male')
        FEMALE = 'Femae', _('Female')
        OTHER = 'Orther', _('Other')

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    phone_number = PhoneNumberField(verbose_name=_('phone number'), max_length=30, default='+2335466789')
    about_me = models.TextField(verbose_name=_('about me'), default='Say something about yourself')
    gender = models.CharField(verbose_name=_('gender'), choices=Gender.choices, default=Gender.MALE, max_length=20)
    country = CountryField(verbose_name=_('country'), default='Gh')
    city = models.CharField(verbose_name=_('city'), max_length=255, default='Accra')
    profile_photo = models.ImageField(verbose_name=_('profile photo'), upload_to='profile/photos', default='default_profile_photo.jpg')

    def __str__(self):
        return f'{self.user.first_name}\'s profile'

