from rest_framework import serializers
from .models import *


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_isbn(self, value):
        if len(value) != 13:
            raise serializers.ValidationError("ISBN must be 13 characters long")
        return value