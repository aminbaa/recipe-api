from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Tag, Ingredient, Recipe, recipe_image_file_path


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
        ingredient = Ingredient.objects.create(user=sample_user(),
                                               name='Cucumber')

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the Recipe object string representation"""
        recipe = Recipe.objects.create(
            user=sample_user(),
            title='Steaks and mushrooms sauce',
            time_minutes=5,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
