from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import catalog, contact, product, add_product

app_name = CatalogConfig.name

urlpatterns = [
    path('', catalog, name='index'),
    path('contact/', contact, name='contact'),
    path('product/<int:pk>/', product, name='product'),
    path('add_product/', add_product, name='add_product'),
]
