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


class Attribute(models.Model):
    size = models.CharField(max_length=20, verbose_name=_('size'))
    color = models.CharField(max_length=20, verbose_name=_('color'))
    count = models.PositiveIntegerField(verbose_name=_('count'))

    class Meta:
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attributes')

    def __str__(self):
        return f'{self.size} --> {self.color}'


class DiscountManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(start_date__lte=timezone.now(),
                                             end_date__gte=timezone.now(),
                                             count__gt=0)


class Discount(TimeStamp):
    name = models.CharField(verbose_name=_('name discount'), max_length=255)
    description = models.TextField(verbose_name=_('description discount'), null=True, blank=True)
    code = models.CharField(verbose_name=_('code discount'), unique=True, max_length=15)
    start_date = models.DateTimeField(verbose_name=_('start_date discount'))
    end_date = models.DateTimeField(verbose_name=_('end_date discount'))
    percent = models.PositiveIntegerField(verbose_name=_('percent discount'),
                                          validators=[MinValueValidator(1), MaxValueValidator(100)],
                                          null=True, blank=True)
    amount = models.PositiveIntegerField(verbose_name=_('amount discount'), null=True, blank=True)
    count = models.PositiveIntegerField(verbose_name=_('count discount'), null=True,
                                        blank=True)

    def clean(self):
        if self.percent is not None and self.amount is not None:
            raise ValidationError(_('Only one of percent or amount should be provided.'))
        if self.percent is None and self.amount is None:
            raise ValidationError(_('One of percentage or amount must have a value.'))

    class Meta:
        verbose_name = _(' discount')
        verbose_name_plural = _('discounts')

    objects = models.Manager()
    discount_manage = DiscountManager()

    def __str__(self):
        return f'{self.code} for {self.name}'
