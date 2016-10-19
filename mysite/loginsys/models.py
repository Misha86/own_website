from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import  get_user_model

from django.conf import settings

from django.utils.translation import ugettext_lazy as _
import os

from django.core.files import File

def upload_location(instance, filename):
    path = 'upload/profile_images'
    profile = Profile.objects.order_by("user_id").last()
    if instance.user_id is not None:
        return os.path.join(path, str(instance.user_id), str(filename))
    if not profile:
        return os.path.join(path, 'FIRST_Profile', str(filename))
    if profile.user_id is not None:
        new_id = profile.user_id + 1
        return os.path.join(path, str(new_id), str(filename))


class ProfileManager(models.Manager):

    # def get_by_natural_key(self, first_name, last_name):
    #     return self.get(user__first_name=first_name, user__last_name=last_name)

    def get_by_natural_key(self, first_name, last_name):
        profile = self.get(user__first_name=first_name, user__last_name=last_name)
        return profile.user.get_full_name()


class Profile(models.Model):
    objects = ProfileManager()

    class Meta:
        db_table = "profile"
        verbose_name = _("Профіль користувача")
        verbose_name_plural = _("Профілі користувачів")

    # user = models.OneToOneField(User, primary_key=True, related_name="profile", verbose_name=_("Користувач"),
    #                             on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, related_name="profile", verbose_name=_("Користувач"),
                                on_delete=models.CASCADE, unique=True)
    sex = models.CharField(max_length=20, choices=(('Man', _('Чоловік')), ('Woman', _('Жінка'))),
                           verbose_name=_("Стать"))
    avatar = models.ImageField(verbose_name=_("Аватарка"), upload_to=upload_location, blank=True,
                               help_text=_("Фото користувача"))
    profile_create = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата створення профіля"))
    profile_update = models.DateTimeField(auto_now=True, verbose_name=_("Дата оновлення профіля"))
    date_of_birth = models.DateField(blank=True, null=True, verbose_name=_("Дата народження"))

    def __str__(self):
        return self.user.get_full_name()

    def natural_key(self):                 # natural key for serialization also for serialization for manage.py dumpdata --natural-foreign
        return self.user.get_full_name()




