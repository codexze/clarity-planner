from rest_framework import serializers
from .models import Gender, Client

class GenderSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField()

    @classmethod
    def get_choices(cls):
        return [{"key": gender.name, "value": gender.value} for gender in Gender]
    
    @classmethod
    def get_choice(cls, gender_value):
        for gender in Gender:
            if gender.value == gender_value:
                return {"key": gender.name, "value": gender.value}
        return None  # Return None if not found

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'