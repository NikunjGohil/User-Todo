from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import gettext as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, user_email, password, **extra_fields):

        if not user_email:
            raise ValueError(_('The Email must be set'))
        if not password:
            raise ValueError(' User must have a password')
        user = self.model(user_email=user_email, **extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, user_email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(user_email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=255, blank=True, null=True, default=None)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10}$',
                                 message="Phone number must be entered in proper format in 10 digits.")
    user_phone = models.CharField(validators=[phone_regex], max_length=15)
    first_name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    image = models.ImageField( upload_to=None, height_field=None, width_field=None, max_length=None, null=True,blank=True)
    address = models.CharField(max_length=300,null=True,blank=True)
    city = models.CharField(max_length=50,null=True,blank=True)
    state = models.CharField(max_length=50,null=True,blank=True)
    Pin_Code = models.IntegerField(null=True,blank=True)
    user_email = models.EmailField('email address', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_email_verified = models.BooleanField(default=False)
    is_premium_activated = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.user_email


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo_title = models.CharField(max_length=200)
    todo_description = models.TextField(blank=True, null=True)
    is_done = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    favourite = models.BooleanField(default=False)

    def __str__(self):
        return self.todo_title


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# class favourite(models.Model):
#     todo=models.ForeignKey(Todo, on_delete=models.CASCADE)
#     user=models.ForeignKey(User ,on_delete=models.CASCADE)
#     is_favourite=models.BooleanField(default=False)



