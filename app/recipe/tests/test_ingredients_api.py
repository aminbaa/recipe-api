from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):
    """Tests the publicly available ingredients Api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Test the private ingredient API"""

    def setUp(self):
        self.client = APIClient()
        user = get_user_model().objects.create_user(
            'test@test.com',
            'password123'
        )
        self.user = user
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients_list(self):
        """Test retrieve a list of ingredients"""
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='salt')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Tests that only ingredients for the
        authenticated user are retrieved"""

        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='salt')
        other_user = get_user_model().objects.create_user(
            'other@test.com', 'password123'
        )
        Ingredient.objects.create(user=other_user, name='vinegar')
        user_ingredients = Ingredient.objects.filter(
            user=self.user).order_by('-name')
        serializer = IngredientSerializer(user_ingredients, many=True)

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_ingredient_successful(self):
        """Test create a new ingredient"""
        payload = {'name': 'salt'}
        res = self.client.post(INGREDIENTS_URL, payload)
        exist = Ingredient.objects.filter(user=self.user, name=payload['name']).exists()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exist)

    def test_create_ingredient_invalid(self):
        """Test creating invalid ingredient fails"""
        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)
        self.assertEqual(res.status_code,
                         status.HTTP_400_BAD_REQUEST)
