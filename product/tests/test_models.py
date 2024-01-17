from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime
from django.utils.text import slugify
from product.models import Product, Attribute, Comment, Category, Image, Discount, Like
from django.core.exceptions import ValidationError


class CategoryModelTest(TestCase):

    def setUp(self):
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

    def test_category_str(self):
        category = self.test_category
        print()
        self.assertEqual(str(category), f'{category.name}')

    def test_parent_category(self):
        self.assertEqual(self.test_category.replay_cat, self.test_parent)

    def test_save_method_with_slug(self):
        self.assertEqual(self.test_parent.slug, 'first Test Category')

    def test_soft_delete(self):
        self.test_category.delete()
        self.assertTrue(self.test_category.is_deleted)

    def test_undelete_method(self):
        self.test_category.is_deleted = True
        self.test_category.save()
        self.test_category.undelete()
        self.assertFalse(self.test_category.is_deleted)

    def test_hard_delete_method(self):
        self.test_category.hard_delete()
        self.assertFalse(Category.objects.filter(id=self.test_category.id).exists())


class AttributeModelTest(TestCase):

    def setUp(self):
        self.attribute = Attribute.objects.create(
            size=36,
            color='Red',
            count=5
        )

    def test_str_method(self):
        test_str = f'{self.attribute.size} --> {self.attribute.color}'
        self.assertEqual(str(self.attribute), test_str)


class DiscountModelTest(TestCase):
    def setUp(self):
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

    def test_discount_str(self):
        test_str = f'{self.discount.code} for {self.discount.name}'
        self.assertEqual(str(self.discount), test_str)

    def test_clean_method_with_both_percent_and_amount(self):
        self.discount.percent = 10
        self.discount.amount = 20
        with self.assertRaises(ValidationError):
            self.discount.full_clean()

    def test_clean_method_with_neither_percent_nor_amount(self):
        self.discount.percent = None
        self.discount.amount = None
        with self.assertRaises(ValidationError):
            self.discount.full_clean()

    def test_active_discounts(self):
        active_discounts = Discount.discount_manage.all()
        self.assertEqual(active_discounts.count(), 1)


class ProductModelTest(TestCase):

    def setUp(self):

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

    def test_str_method(self):
        test_str = self.product.name
        self.assertEqual(str(self.product), test_str)

    def test_product_slug(self):
        slug = slugify(self.product.name)
        self.assertEqual(self.product.slug, slug)

    def test_save_method(self):
        self.product.price = 120
        self.product.save()
        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.price, 120)

    def test_archive_manager(self):
        archived_products = Product.objects.archive()
        self.assertEqual(archived_products.count(), 1)

    def test_deleted_manager(self):
        deleted_products = Product.objects.deleted()
        self.assertEqual(deleted_products.count(), 0)

    def test_hard_delete_method(self):
        self.product.delete()
        deleted_products = Product.objects.deleted()
        self.assertEqual(deleted_products.count(), 1)


class ImageModelTest(TestCase):
    def setUp(self):
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

        self.image = Image.objects.create(
            image='item_image/test_image.jpg',
            product=self.product
        )

    def test_str_method(self):
        test_str = f'{self.image.product.name}'
        self.assertEqual(str(self.image), test_str)

    def test_related_name(self):
        images = self.product.images.all()
        self.assertEqual(images.count(), 1)


class LikeModelTest(TestCase):
    def setUp(self):
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

        self.user = get_user_model().objects.create(
            email='abolfazlrasouli@gmail.com',
            phone_number='09121234567',
            birthday='2000-01-01',
            role=get_user_model().CUSTOMERUSER_CUSTOMER,
            is_deleted=False,
            username='abolfazl',
            password='123456zx!'
        )

        self.like = Like.objects.create(
            product=self.product,
            user=self.user
        )

    def test_str_method(self):
        test_str = f'{self.user.username}: {self.product.name}'
        self.assertEqual(str(self.like), test_str)

    def test_related_name(self):
        likes = self.product.product_like.all()
        self.assertEqual(likes.count(), 1)

    def test_logical_queryset(self):

        deleted_like = self.like
        deleted_like.delete()

        deleted_likes = Like.objects.deleted()
        self.assertEqual(deleted_likes.count(), 1)

        archive_likes = Like.objects.archive()
        self.assertEqual(archive_likes.count(), 1)

    def test_undelete_method(self):

        self.like.delete()
        self.assertTrue(self.like.is_deleted)

        self.like.undelete()
        self.assertFalse(self.like.is_deleted)


class CommentModelTest(TestCase):

    def setUp(self):
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

        self.user = get_user_model().objects.create(
            email='abolfazlrasouli@gmail.com',
            phone_number='09121234567',
            birthday='2000-01-01',
            role=get_user_model().CUSTOMERUSER_CUSTOMER,
            is_deleted=False,
            username='abolfazl',
            password='123456zx!'
        )

        self.comment = Comment.objects.create(
            body='This is a test comment',
            status=Comment.COMMENT_STATUS_WAITING,
            product=self.product,
            user=self.user,
            reply_comment=None
        )

        self.test_comment = Comment.objects.create(
            body='This is a test comment',
            status=Comment.COMMENT_STATUS_WAITING,
            product=self.product,
            user=self.user,
            reply_comment=self.comment
        )

    def test_comment_str(self):
        test_str = f'{self.comment.body} : {self.comment.user}'
        self.assertEqual(str(self.test_comment), test_str)

    def test_comment_delete(self):
        self.comment.delete()
        self.assertTrue(self.comment.is_deleted)

    def test_comment_undelete(self):
        self.comment.delete()
        self.assertTrue(self.comment.is_deleted)

        self.comment.undelete()
        self.assertFalse(self.comment.is_deleted)

    def test_comment_archived_queryset(self):
        archived_comments = Comment.objects.archive()
        self.assertEqual(archived_comments.count(), 2)

        self.comment.delete()
        archived_comments = Comment.objects.archive()
        self.assertEqual(archived_comments.count(), 2)

    def test_comment_deleted_queryset(self):
        deleted_comments = Comment.objects.deleted()
        self.assertEqual(deleted_comments.count(), 0)

        self.comment.delete()
        deleted_comments = Comment.objects.deleted()
        self.assertEqual(deleted_comments.count(), 1)

