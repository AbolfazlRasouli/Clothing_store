from django.db import models
from apps.accounts.models import Address
from django.conf import settings
from apps.core.models import TimeStamp, BaseModel
from apps.product.models import Product
from django.utils.translation import gettext_lazy as _


class Order(TimeStamp, BaseModel):
    ORDER_STATUS_PAID = 'p'
    ORDER_STATUS_UNPAID = 'u'
    ORDER_STATUS_CANCELED = 'c'
    ORDER_STATUS = (
        (ORDER_STATUS_PAID, 'Paid'),
        (ORDER_STATUS_UNPAID, 'Unpaid'),
        (ORDER_STATUS_CANCELED, 'Canceled'),
    )

    status = models.CharField(max_length=1, choices=ORDER_STATUS,
                              verbose_name=_('status order'),
                              default=ORDER_STATUS_UNPAID)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='order_user',
                             verbose_name=_('user'))
    address = models.ForeignKey(Address, on_delete=models.CASCADE,
                                null=True, blank=True,
                                related_name='order_adders',
                                verbose_name=_('Address'))

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):
        return f'{self.user} : {self.status}'


class OrderItem(BaseModel):
    size = models.CharField(max_length=20, verbose_name=_('size'))
    color = models.CharField(max_length=20, verbose_name=_('color'))
    count = models.PositiveIntegerField(verbose_name=_('count'))
    price = models.PositiveIntegerField(verbose_name=_('price'))
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='orderitem_order',
                              verbose_name=_('order'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='orderitem_product',
                                verbose_name=_('product '))

    class Meta:
        verbose_name = _('order item')
        verbose_name_plural = _('order items')

    def __str__(self):
        return f'{self.order} : {self.product}'
