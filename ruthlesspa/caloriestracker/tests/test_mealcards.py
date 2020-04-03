from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib import auth

from rest_framework.test import APIClient
from rest_framework import status

class PublicMealcardsApiTests(TestCase):
    """Test unauthenticated user MealCards API access"""

    def setUp(self):
        self.client = APIClient()

    
    def test_auth_required_save_mealcards(self):
        pass

    def test_auth_required_get_mealcards(self):
        pass

    def test_auth_required_calories_stats(self):
        pass

    def test_auth_required_search_by_foodname(self):
        """That one is already failing for now"""
        pass


class PrivateMealcardsApiTests(TestCase):
    """Test authenticated user mealcard manipulation functionality"""

    def setUp(self):

        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@dctest.com',
            'dctestpass'
        )
        self.user.is_active = 1
        self.client.force_authenticate(self.user)

    def test_retrieve_mealcards_success(self):
        pass

    def test_mealcards_limited_to_user(self):
        pass

    def test_created_mealcards_retrievable(self):
        """User creates mealcards and is able to get them by date"""
        pass

    def test_removing_mealcards(self):
        """User creates two and removes 1 mealcard"""
        pass

    def test_adding_ingredients_to_mealcards(self):
        pass
    
    def test_removing_ingredients(self):
        pass

    def test_removing_mealcards_cascades_ingredients(self):
        pass


class PrivateStatsApiTests(TestCase):
    """Test user stats functionality"""
    
        def setUp(self):

        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@dctest.com',
            'dctestpass'
        )
        self.user.is_active = 1
        self.client.force_authenticate(self.user)

        """setUp needs to cover creating mealcards with added ingredients for the user - SOONish."""



    def test_all_stats_delivered(self):
        """Server delivers all user items"""
        pass

    def test_energy_consumption_calculated_properly(self):
        pass
    
    def test_response_sorted_by_date(self):
        pass
