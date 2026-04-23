# users/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import PerfilUsuario

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name']

    #def create(self, validated_data):
        #user = User.objects.create_user(**validated_data)
        #return user


    def create(self, validated_data):
            password = validated_data.pop("password")
            user = User(**validated_data)
            user.set_password(password)
            user.save()
            return user



#Perfil clínico del paciente
class PerfilUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilUsuario
        fields = '__all__'
