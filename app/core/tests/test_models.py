from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Tag

from core.models import Ingredient


def sample_user(email='test@test.com', name='test_name'):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(email, name)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@test.com'
        password = 'Password123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@TEST.com'
        password = 'Password123'
        user = get_user_model().objects.create_user(email, password)
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        password = 'Password123'
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, password)

    def test_create_new_superuser(self):
        """Test creating a new superuser """
        user = get_user_model().objects.create_superuser(
            'test@TEST.com',
            'Password123'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_tag_str(self):
        """Test the Tag object string representation"""

        tag = Tag.objects.create(user=sample_user(), name='vegan')
        self.assertEqual(str(tag), tag.name)

    def test_ingredients_str(self):
        """Test the Ingredient object string representation"""
        ingredient = Ingredient.objects.create(user=sample_user(), name='Cucumber')

        self.assertEqual(str(ingredient), ingredient.name)
