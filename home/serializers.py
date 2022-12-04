from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Content

class GetContent(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'

class GetUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups']
