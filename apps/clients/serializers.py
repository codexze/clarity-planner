from rest_framework import serializers
from .models import Gender, Client

class GenderSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField()


class ClientSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    display = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = '__all__'

    def get_name(self, obj):
        """Fetches the property from the model"""
        return obj.name  
    
    def get_age(self, obj):
        """Fetches the property from the model"""
        return obj.age  
    
    def get_display(self, obj):
        """Fetches the property from the model"""
        return obj.display