from django.conf import settings
from django.utils import timezone
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from apps.core.models import TimeStamp, BaseModel


# class TimeStamp(models.Model):
#     create_at = models.DateTimeField(verbose_name=_('create_at'), auto_now_add=True)
#     updated_at = models.DateTimeField(verbose_name=_('updated_at'), auto_now=True)
#
#     class Meta:
#         abstract = True
#
#
# class LogicalQuerySet(models.QuerySet):
#
#     def delete(self):
#         print('delete all list queryset')
#         return super().update(is_deleted=True)
#
#     def hard_delete(self):
#         return super().delete()
#
#
# class LogicalManager(models.Manager):
#
#     def logical_queryset(self):
#         return LogicalQuerySet(self.model)
#
#     def get_queryset(self):
#         return self.logical_queryset().filter(is_deleted=False)
#
#     def archive(self):
#         return self.logical_queryset()
#
#     def deleted(self):
#         return self.logical_queryset().filter(is_deleted=True)
#
#
# class BaseModel(models.Model):
#     is_deleted = models.BooleanField(verbose_name=_('delete'), default=False)
#     delete_date = models.DateTimeField(verbose_name=_('delete_date'), null=True, blank=True)
#
#     class Meta:
#         abstract = True
#
#     objects = LogicalManager()
#
#     def delete(self, using=None, keep_parents=False):
#         print('delete only object')
#         self.is_deleted = True
#         self.delete_date = timezone.now()
#         self.save()
#
#     def hard_delete(self):
#         super().delete()
#
#     def undelete(self):
#         self.is_deleted = False
#         self.save()


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
            self.slug = slugify(self.name, allow_unicode=True)
            self.save()
        return super().save(*args, **kwargs)


class Attribute(models.Model):
    size = models.CharField(max_length=20, verbose_name=_('size'))
    name_color = models.CharField(max_length=20, verbose_name=_('name color'))
    code_color = models.CharField(max_length=20, verbose_name=_('code color'))
    count = models.PositiveIntegerField(verbose_name=_('count'))

    class Meta:
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attributes')

    def __str__(self):
        return f'{self.size} --> {self.name_color}'


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


class Product(TimeStamp, BaseModel):
    name = models.CharField(verbose_name=_('name product'), max_length=255)
    brand = models.CharField(verbose_name=_('brand'), max_length=100)
    code = models.CharField(verbose_name=_('code'), max_length=15, unique=True)
    price = models.PositiveIntegerField(verbose_name=_('price product'))
    slug = models.SlugField(verbose_name=_('name unique product'), max_length=100, unique=True, blank=True)
    description = models.TextField(verbose_name=_(' description product'), null=True, blank=True)
    image = models.ImageField(verbose_name=_('image product'), upload_to='item_image/')
    attribute = models.ManyToManyField(Attribute, related_name='product_attribute',
                                       verbose_name=_('attribute product'))
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE,
                                 related_name='product_discount',
                                 null=True, blank=True,
                                 verbose_name=_('discount product'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category',
                                 verbose_name=_('category'))

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def calculate_discounted_price(self):
        if self.discount:
            if self.discount.percent:
                discount_amount = (self.discount.percent / 100) * self.price
            elif self.discount.amount:
                discount_amount = self.discount.amount
            else:
                raise ValidationError(_('Invalid discount type.'))
            return self.price - discount_amount
        else:
            return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class Image(models.Model):
    image = models.ImageField(verbose_name=_('Image'), upload_to='item_image/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Image gallery')

    def __str__(self):
        return f'{self.product.name}'


class Like(TimeStamp, BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='product_like',
                                verbose_name=_('product'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='user_like',
                             verbose_name=_('user'))

    class Meta:
        verbose_name = _('like')
        verbose_name_plural = _('likes')

    def __str__(self):
        return f'{self.user.username}: {self.product.name}'


class Comment(TimeStamp, BaseModel):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'na'
    COMMENT_STATUS = (
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
        (COMMENT_STATUS_NOT_APPROVED, 'Not Approved'),
    )
    body = models.TextField(verbose_name=_('comment text'))
    status = models.CharField(max_length=2, choices=COMMENT_STATUS,
                              default=COMMENT_STATUS_WAITING,
                              verbose_name=_('comment status'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='product_comments',
                                verbose_name=_('comment product'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='user_comments',
                             verbose_name=_('comment user'))
    reply_comment = models.ForeignKey('self', on_delete=models.CASCADE,
                                      null=True, blank=True,
                                      related_name='replize_comment',
                                      verbose_name=_('replize comment'))

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        return f'{self.body} : {self.user}'
