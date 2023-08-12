from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contact, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('contact/', contact, name='contact'),
    path('', ProductListView.as_view(), name='index'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('product_create/', ProductCreateView.as_view(), name='product_create'),
    path('product_update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product_delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('blogs/', BlogListView.as_view(), name='blogs'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog'),
    path('add_blog/', BlogCreateView.as_view(), name='add_blog'),
    path('blog/update/<slug:slug>/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/delete/<slug:slug>/', BlogDeleteView.as_view(), name='blog_delete'),
]
