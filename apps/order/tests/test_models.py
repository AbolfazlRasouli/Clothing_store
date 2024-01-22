from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.product.models import Product, Attribute, Category, Discount
from apps.accounts.models import Address
from apps.order.models import Order, OrderItem


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            email='abolfazlrasouli@gmail.com',
            phone_number='09121234567',
            birthday='2000-01-01',
            role=get_user_model().CUSTOMERUSER_CUSTOMER,
            is_deleted=False,
            username='abolfazl',
            password='123456zx!'
        )
        self.address = Address.objects.create(
            user=self.user,
            country='Iran',
            province='Tehran',
            city='Tehran',
            street='Main Street',
            pelak='1234',
            complete_address='Main Street, Tehran, Iran'
        )
        self.order = Order.objects.create(
            status=Order.ORDER_STATUS_UNPAID,
            user=self.user,
            address=self.address,
        )

    def test_delete_soft(self):
        self.assertFalse(self.order.is_deleted)
        self.order.delete()
        self.assertTrue(self.order.is_deleted)

    def test_undelete(self):
        self.order.delete()
        self.assertTrue(self.order.is_deleted)
        self.order.undelete()
        self.assertFalse(self.order.is_deleted)

    def test_order_with_past_start_date(self):
        past_start_date = timezone.now() - timezone.timedelta(days=1)
        self.order.start_date = past_start_date
        self.order.save()
        self.assertEqual(self.order.start_date, past_start_date)

    def test_order_update_status(self):
        new_status = Order.ORDER_STATUS_PAID
        self.order.status = new_status
        self.order.save()
        updated_order = Order.objects.get(id=self.order.id)
        self.assertEqual(updated_order.status, new_status)

    def test_order_str(self):
        order = self.order
        self.assertEqual(str(order), f'{order.user} : {order.status}')

    def test_order_status(self):
        order = self.order
        self.assertEqual(order.status, Order.ORDER_STATUS_UNPAID)


class OrderItemModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            email='abolfazlrasouli@gmail.com',
            phone_number='09121234567',
            birthday='2000-01-01',
            role=get_user_model().CUSTOMERUSER_CUSTOMER,
            is_deleted=False,
            username='abolfazl',
            password='123456zx!'
        )
        self.address = Address.objects.create(
            user=self.user,
            country='Iran',
            province='Tehran',
            city='Tehran',
            street='Main Street',
            pelak='1234',
            complete_address='Main Street, Tehran, Iran'
        )
        self.order = Order.objects.create(
            status=Order.ORDER_STATUS_UNPAID,
            user=self.user,
            address=self.address,
        )

        self.test_parent = Category.objects.create(
            name='first Test Category',
            description='This is a test category',
            slug='first Test Category',
            image='category_image/test_image.jpg'
        )

        self.test_category = Category.objects.create(
            name='second Test Category',
            description='This is a test category',
            slug='second Test Category',
            image='category_image/test_image.jpg',
            replay_cat=self.test_parent
        )
        self.discount = Discount.objects.create(
            name='Test Discount',
            description='test discount',
            code='TESTCODE',
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=7),
            percent=10,
            amount=None,
            count=5
        )
        self.attribute = Attribute.objects.create(
            size=36,
            color='Red',
            count=5
        )
        self.product = Product.objects.create(
            name='Test Product',
            brand='Test Brand',
            code='Test001',
            price=100,
            slug='test-product',
            description='This is a test product',
            image='item_image/test_image.jpg',
            # attribute=self.attribute,
            discount=self.discount,
            category=self.test_category
        )
        self.product.attribute.add(self.attribute)

        self.order_item = OrderItem.objects.create(
            size='32',
            color='blue',
            count=2,
            price=50,
            order=self.order,
            product=self.product,
        )

    def test_order_item_creation(self):
        self.assertTrue(isinstance(self.order_item, OrderItem))
        self.assertEqual(str(self.order_item), f'{self.order_item.order} : {self.order_item.product}')

    def test_order_item_count(self):
        self.assertEqual(self.order_item.count, 2)

    def test_order_item_price(self):
        self.assertEqual(self.order_item.price, 50)

    def test_order_item_update(self):
        new_count = 4
        self.order_item.count = new_count
        self.order_item.save()
        self.assertEqual(self.order_item.count, new_count)

    def test_manager_logical_queryset(self):
        queryset = OrderItem.objects.deleted()
        self.assertEqual(queryset.count(), 0)

    def test_manager_archive(self):
        queryset = OrderItem.objects.archive()
        self.assertEqual(queryset.count(), 1)

    def test_model_delete(self):
        obj = OrderItem.objects.first()
        obj.delete()
        self.assertTrue(obj.is_deleted)
