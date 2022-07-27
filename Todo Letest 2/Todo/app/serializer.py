from rest_framework.validators import UniqueValidator
import django.contrib.auth.password_validation as validators
from rest_framework import serializers
from .models import Todo, User
from rest_framework.authtoken.models import Token
import logging

logger = logging.getLogger(__name__)


class Todoserializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "todo_title", "todo_description", "create_at", "is_done", "favourite"]
        read_only_fields = ["user", "create_at"]


        # def update(self, instance, validated_data):
        #     print ('thishere')
        #     demo = Todo.objects.get(pk=instance.id)
        #     Todo.objects.filter(pk=instance.id).update(**validated_data)


class Todo_Update(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "favourite"]
        read_only_fields = ["user", "todo_title", "todo_description", "create_at", "is_done"]


class SignupSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ["user_email", "password"]

    # def create(self, validated_data):
    #     #validated_data['user_phone'] = self.context.get('user_phone')
    #     validated_data['user_email'] = self.context.get('user_email')
    #     validated_data['password'] = self.context.get('password')
    #     user_instance = User.objects.create_user(**validated_data)
    #     return user_instance


class UserLoginSerializer(serializers.Serializer):
    user_email = serializers.EmailField()
    password = serializers.CharField()
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        token = Token.objects.get_or_create(user=obj)[0]
        logger.error(token.key)
        return token.key

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # read_only_fields = [""]
        fields =["id","first_name","last_name","image","user_phone","address","city","state","Pin_Code"]
        

    
    # def update(self, instance, validated_data):
    #     print(instance)
    #     user_instance = super(UserSerializer, self).update(instance, validated_data)
    #     return user_instance
        # instance.first_name = validated_data.get('first_name',instance.first_name)
        # instance.first_name = validated_data.get('first_name',instance.first_name)
        # instance.first_name = validated_data.get('first_name',instance.first_name)
        # instance.first_name = validated_data.get('first_name',instance.first_name)
        # instance.first_name = validated_data.get('first_name',instance.first_name)
        # instance.first_name = validated_data.get('first_name',instance.first_name)
        # instance.first_name = validated_data.get('first_name',instance.first_name)
        # instance.first_name = validated_data.get('first_name',instance.first_name)