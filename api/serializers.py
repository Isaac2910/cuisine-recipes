
from rest_framework import serializers
from .models import User, Recipe


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name', 'email', 'password', 'phone']




 
##########User configuration


################################################################Recipes
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['title', 'image', 'description', 'ingredients']

        

