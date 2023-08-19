from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from pytils.translit import slugify

NULLABLE = {'blank': True, 'null':True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.CharField(max_length=100, verbose_name='Описание')
    #created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория товара')
    price = models.IntegerField(verbose_name='Цена за покупку')
    create_date = models.DateTimeField(verbose_name='Дата создания',auto_now_add=True)
    last_change_date = models.DateTimeField(verbose_name='Дата последнего изменения', auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Владелец')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('catalog:product', args=[str(self.id)])

    def active_version(self):
        return self.version_set.get(is_active=True)

    class Meta:
        permissions = [
            (
                'set_published',
                'Может отменять публикацию продукта'
            ),
            (
                'set_description',
                'Может менять описание любого продукта'
            ),
            (
                'set_category',
                'Может менять категорию любого продукта'
            )
        ]
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class Version(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    number = models.IntegerField(verbose_name='Номер версии')
    title = models.CharField(max_length=100, verbose_name='Название версии')
    is_active = models.BooleanField(default=False, verbose_name='Признак текущей версии')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'

    def clean(self) -> None:
        super().clean()
        if Version.objects.filter(product=self.product, is_active=True).get() != self and self.is_active :
            raise forms.ValidationError('Ты можешь установить только одну активную версию.')


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, **NULLABLE)
    content = models.TextField(verbose_name='Cодержимое')
    image = models.ImageField(upload_to='blog/', verbose_name='Изображение', **NULLABLE)
    create_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    is_published = models.BooleanField(verbose_name='Признак публикации')
    count_views = models.IntegerField(verbose_name='Количество просмотров', default=0)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("catalog:blog", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            for blog in Blog.objects.all():
                if blog.slug == slug:
                    slug = f'{slug}_'
            self.slug = slug
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_published = False
        self.save()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-create_date']
