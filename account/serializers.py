from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from account.utils import send_activation_mail
from myprofile.models import ProfileMaster, ProfileCustomer

MyUser = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True, required=True)
    password_confirm = serializers.CharField(min_length=8, write_only=True, required=True)

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'password_confirm', 'status')

    def validate_email(self, email):
        if MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с данным email уже существует')
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm', None)
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self, validated_data):
        user = MyUser.objects.create_user(**validated_data)
        send_activation_mail(user.email, user.activation_code)
        if user.status == 'master':
            ProfileMaster.objects.create(user=user, email=user.email)
        else:
            ProfileCustomer.objects.create(user=user, email=user.email)
        return user


class CreateNewPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150, required=True)
    activation_code = serializers.CharField(max_length=6, min_length=6, required=True)
    password = serializers.CharField(min_length=8, required=True)
    password_confirm = serializers.CharField(min_length=8, required=True)

    def validate_email(self, email):
        if not MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователя с таким email не найден')
        return email

    def validate_activation_code(self, code):
        if not MyUser.objects.filter(activation_code=code, is_active=False).exists():
            raise serializers.ValidationError('Неверный код активации')
        return code

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        email = data.get('email')
        code = data.get('activation_code')
        password = data.get('password')
        try:
            user = MyUser.objects.get(email=email, activation_code=code, is_active=False)
        except MyUser.DoesNotExist:
            raise serializers.ValidationError('Пользователь не найден')
        user.is_active = True
        user.activation_code = ''
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
