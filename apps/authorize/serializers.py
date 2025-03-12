from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    display = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'display','name', 'first_name', 'last_name', 'date_of_birth', 'age','email', 'is_staff', 'is_active', 'groups']

    def get_name(self, obj):
        """Fetches the property from the model"""
        return obj.name  
    
    def get_age(self, obj):
        """Fetches the property from the model"""
        return obj.age  
    
    def get_display(self, obj):
        """Fetches the property from the model"""
        return obj.display
    
class UserLimitedSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'username', 'name']