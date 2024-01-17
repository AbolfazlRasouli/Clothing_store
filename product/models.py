from django.conf import settings
from django.utils import timezone
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError


class TimeStamp(models.Model):
    create_at = models.DateTimeField(verbose_name=_('create_at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated_at'), auto_now=True)

    class Meta:
        abstract = True


class LogicalQuerySet(models.QuerySet):

    def delete(self):
        print('delete all list queryset')
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


class Category(TimeStamp, BaseModel):
    name = models.CharField(verbose_name=_('name category'), max_length=100, unique=True)
    description = models.TextField(verbose_name=_('description category'), null=True, blank=True)
    slug = models.SlugField(verbose_name=_('name unique category'), max_length=100, unique=True, blank=True)
    image = models.ImageField(verbose_name=_('image category'), upload_to='category_image/')
    replay_cat = models.ForeignKey('self', null=True, blank=True,
                                   on_delete=models.CASCADE,
                                   related_name='replize_category')

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            self.save()
        return super().save(*args, **kwargs)
