from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')

    phone = models.CharField(max_length=12, verbose_name='Номер телефона', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='Страна', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    register_uuid = models.CharField(max_length=50, **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
