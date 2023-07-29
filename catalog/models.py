from django.db import models
from django.urls import reverse
from pytils.translit import slugify

NULLABLE = {'blank': True, 'null':True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.CharField(max_length=100, verbose_name='Описание')

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

    def get_absolute_url(self):
        return reverse('catalog:product', args=[str(self.id)])

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, **NULLABLE)
    content = models.TextField(verbose_name='Cодержимое')
    image = models.ImageField(upload_to='blog/', verbose_name='Изображение', **NULLABLE)
    create_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    is_published = models.BooleanField(verbose_name='Подтвердить публикацию')
    count_views = models.IntegerField(verbose_name='Количество просмотров', default=0)

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
