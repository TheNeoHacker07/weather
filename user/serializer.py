from rest_framework import serializers
from django.contrib.auth import get_user_model
from .email import send_activation_code  

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=4, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=4, required=True, write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')

        
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают!')
        
    
        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            raise serializers.ValidationError('Пароль должен быть не менее 8 символов и содержать как буквы, так и цифры.')
        
        return attrs
    
    #метод для создания пользавателя  
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            second_name=validated_data.get('second_name', '')
        )
        send_activation_code(user.email, user.activation_code)
        return user
