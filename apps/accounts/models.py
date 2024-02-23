from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .validation import validate_birthday, validate_image
from apps.core.models import LogicalManager
from django.contrib.auth.models import UserManager
from django.contrib.auth import get_user_model
from apps.core.models import UserRelatedModelBaseManager
from django.contrib.auth.models import Group, Permission


class UserLogicalManager(UserManager, LogicalManager):

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_active", True)
        return super().create_superuser(username, email, password, **extra_fields)


class CustomUser(AbstractUser):

    CUSTOMERUSER_EMPLOYEE = 'e'
    CUSTOMERUSER_CUSTOMER = 'c'
    CUSTOMERUSER_MANAGER = 'm'
    CUSTOMERUSER_STATUS = (
        (CUSTOMERUSER_EMPLOYEE, "employee"),
        (CUSTOMERUSER_CUSTOMER, "customer"),
        (CUSTOMERUSER_MANAGER, "manager"))

    email = models.EmailField(verbose_name=_('Email Address'), unique=True)
    mobile_regex = RegexValidator(regex='^09[0-9]{9}$',
                                  message="Phone number must be entered in the format: '09199999933'.")
    phone_number = models.CharField(validators=[mobile_regex],
                                    verbose_name=_('phone number'),
                                    max_length=11, unique=True)
    birthday = models.DateField(verbose_name=_('birthday'),
                                blank=True, null=True,
                                validators=[validate_birthday])
    profile_image = models.ImageField(upload_to='profile_image/',
                                      verbose_name=_('profile image'),
                                      blank=True, null=True,
                                      validators=[validate_image])
    is_deleted = models.BooleanField(verbose_name=_('is_deleted'), default=False)
    is_active = models.BooleanField(verbose_name=_('is_active'), default=False)
    user_type = models.CharField(max_length=1, choices=CUSTOMERUSER_STATUS, default=CUSTOMERUSER_CUSTOMER)

    REQUIRED_FIELDS = ['email', 'phone_number']

    objects = UserLogicalManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.user_type == CustomUser.CUSTOMERUSER_EMPLOYEE and self.is_active:
            group, created = Group.objects.get_or_create(name="operator")
            if created:
                perm = Permission.objects.filter(codename__in=[
                    'add_customuser', 'change_customuser', 'delete_customuser', 'view_customuser',
                    'add_order', 'change_order', 'delete_order', 'view_order',
                    'add_address' 'change_address', 'delete_address', 'view_address'
                ])
                group.permissions.add(*perm)
            self.groups.add(group)

        if self.user_type == CustomUser.CUSTOMERUSER_MANAGER and self.is_active:
            group, created = Group.objects.get_or_create(name="manager")
            if created:
                perm = Permission.objects.filter(codename__in=[
                    'add_product', 'change_product', 'delete_product', 'view_product',
                    'add_category', 'change_category', ' delete_category', 'view_category',
                    'add_discount', 'change_discount', 'delete_discount', 'view_discount'
                ])
                group.permissions.add(*perm)
            self.groups.add(group)
            # self.save()
            # print(self.groups.all())

    # def clean(self):
    #    if self.profile_image:
    #         width, height = self.profile_image.width, self.profile_image.height
    #         if width != height:
    #             raise ValidationError({
    #                 'profile_image': _('image : the image must be square ')
    #             })

    def delete(self, using=None, keep_parents=False):
        # print('delete only object')
        self.is_deleted = True
        self.save()

    def undelete(self):
        self.is_deleted = False
        self.save()

    def __str__(self):
        return self.email

    def hard_delete(self):
        return super().delete()


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    country = models.CharField(verbose_name=_('country'), max_length=50)
    province = models.CharField(verbose_name=_('province'), max_length=50)
    city = models.CharField(verbose_name=_('city'), max_length=50)
    street = models.CharField(verbose_name=_('street'), max_length=50)
    pelak = models.CharField(verbose_name=_('pelak'), max_length=4)
    complete_address = models.TextField(verbose_name=_('complete_address'), max_length=500)

    objects = UserRelatedModelBaseManager()

    def __str__(self):
        return f'{self.user} - {self.city} - {self.street}'

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Address')
