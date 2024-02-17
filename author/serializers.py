from rest_framework import serializers

from .models import Authors


class AuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = '__all__'
        read_only_fields = (
            'slug', 'created_at', 'updated_at'
        )
