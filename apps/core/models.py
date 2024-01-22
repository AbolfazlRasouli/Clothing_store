from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager
from django.conf import settings
from django.utils import timezone


class LogicalQuerySet(models.QuerySet):
    def delete(self):
        # print('delete all list queryset')
        return super().update(is_deleted=True)

    def hard_delete(self):
        return super().delete()


class LogicalManager(models.Manager):
    def logical_queryset(self):
        return LogicalQuerySet(self.model)

    def get_queryset(self):
        return self.logical_queryset().filter(is_deleted=False)

    def archive(self):
        return self.logical_queryset()

    def deleted(self):
        return self.logical_queryset().filter(is_deleted=True)


class TimeStamp(models.Model):
    create_at = models.DateTimeField(verbose_name=_('create_at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated_at'), auto_now=True)

    class Meta:
        abstract = True


class BaseModel(models.Model):
    is_deleted = models.BooleanField(verbose_name=_('delete'), default=False)
    delete_date = models.DateTimeField(verbose_name=_('delete_date'), null=True, blank=True)

    class Meta:
        abstract = True

    objects = LogicalManager()

    def delete(self, using=None, keep_parents=False):
        print('delete only object')
        self.is_deleted = True
        self.delete_date = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()

    def undelete(self):
        self.is_deleted = False
        self.save()


class UserRelatedModelBaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user__is_deleted=False)


