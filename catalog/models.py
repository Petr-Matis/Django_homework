from django.db import models


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
    description = models.CharField(max_length=300, verbose_name='Описание')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='цена за покупку')
    create_date = models.DateTimeField(verbose_name='дата создания',auto_now_add=True)
    last_change_date = models.DateTimeField(verbose_name='дата последнего изменения', auto_now=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
