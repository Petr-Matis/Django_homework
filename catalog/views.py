from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from catalog.models import Product, Category, Blog
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage


class ProductListView(generic.ListView):
    paginate_by = 3
    model = Product
    extra_context = {
        'title': 'Главное меню "Каталог"'
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        all_product = Product.objects.all()
        context['all_product_list'] = all_product
        return context


class ProductDetailView(generic.DetailView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        all_product = Product.objects.all()
        context['all_product_list'] = all_product
        context['title'] = context['object']
        return context


class ProductCreateView(generic.CreateView):
    model = Product
    extra_context = {
        'title': 'Добавить товар'
    }
    fields = ('name', 'description', 'image', 'category', 'price')

    # success_url = reverse_lazy('catalog:index')
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        all_product = Product.objects.all()
        context['all_product_list'] = all_product
        category_list = Category.objects.all()
        context['category_list'] = category_list
        return context


def contact(request):
    products_list = Product.objects.all()
    context = {
        'object_list': products_list,
        'title': 'Контакты'
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'You have new message from {name}({email}): {message}')
    return render(request, 'catalog/contact.html', context)


class BlogListView(generic.ListView):
    model = Blog
    extra_context = {
        'title': 'Блог'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        all_product = Product.objects.all()
        context['all_product_list'] = all_product
        return context


class BlogDetailView(generic.DetailView):
    model = Blog

    def get_context_data(self, *args, **kwargs):
        blog = Blog.objects.get(pk=self.object.pk)
        blog.count_views += 1
        blog.save()
        context = super().get_context_data(*args, **kwargs)
        all_product = Product.objects.all()
        context['all_product_list'] = all_product
        context['title'] = context['object']
        return context


class BlogCreateView(generic.CreateView):
    model = Blog
    extra_context = {
        'title': 'Добавить пост'
    }
    fields = ('title', 'content', 'image', 'is_published',)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        all_product = Product.objects.all()
        context['all_product_list'] = all_product
        return context


class BlogUpdateView(generic.UpdateView):
    model = Blog
    fields = ('title', 'content', 'image', 'is_published',)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        all_product = Product.objects.all()
        context['all_product_list'] = all_product
        context['title'] = context['object']
        return context


class BlogDeleteView(generic.DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blogs')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        all_product = Product.objects.all()
        context['all_product_list'] = all_product
        context['title'] = context['object']
        return context
