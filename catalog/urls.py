from django.urls import path

from catalog.views import catalog, contact

urlpatterns = [
    path('', catalog),
    path('contact/', contact),
]
#include('catalog.urls', namespace='catalog')