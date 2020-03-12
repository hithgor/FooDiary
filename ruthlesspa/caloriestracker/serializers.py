from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Ingredient, CaloriesCard

class IngredientSerializer(serializers.ModelSerializer):
    """Serializers for ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ('name', 'energy',)
        #read_only_fields = ('id')


class MealSerializer(serializers.ModelSerializer):
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    
    class Meta:
        model = CaloriesCard
        fields = ('id', 'title', 'ingredients')
        read_only_fields = ('id',)
