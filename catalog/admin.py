from django.contrib import admin

from catalog.models import Product, Category, Blog



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'content', 'image', 'create_date', 'is_published', 'count_views',)
    fields = ('title', 'content', 'image', 'is_published',)
    list_filter = ('is_published',)
    search_fields = ('title', 'is_published', 'count_views')
    sortable_by = ('create_date',)

