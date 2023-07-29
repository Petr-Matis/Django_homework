from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contact,  ProductListView, ProductDetailView, ProductCreateView, \
    BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('contact/', contact, name='contact'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('add_product/', ProductCreateView.as_view(), name='add_product'),
    path('blogs/', BlogListView.as_view(), name='blogs'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog'),
    path('add_blog/', BlogCreateView.as_view(), name='add_blog'),
    path('blog/update/<slug:slug>/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/delete/<slug:slug>/', BlogDeleteView.as_view(), name='blog_delete'),
]
