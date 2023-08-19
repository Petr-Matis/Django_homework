from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Category, Blog, Version
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
        context['version_is_active'] = Version.objects.filter(is_active=True) # Product.active_version()
        return context


class ProductDetailView(generic.DetailView):
    model = Product
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        all_product = Product.objects.all()
        context['all_product_list'] = all_product
        context['title'] = context['object']
        context['is_edit'] = True
        if self.object.owner != self.request.user and not self.request.user.is_superuser and not self.request.user.is_staff:
            context['is_edit'] = False
        return context


class ProductCreateView(PermissionRequiredMixin, generic.CreateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.add_product'
    extra_context = {
        'title': 'Добавить товар'
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        all_product = Product.objects.all()
        context['all_product_list'] = all_product
        category_list = Category.objects.all()
        context['category_list'] = category_list
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductUpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = Product
    form_class = ProductForm
    permission_required = ['catalog.change_product']
    # fields = ('name', 'description', 'image', 'category', 'price')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        all_product = Product.objects.all()
        context['all_product_list'] = all_product
        category_list = Category.objects.all()
        context['category_list'] = category_list
        context['title'] = context['object']
        version_form_set = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context['formset'] = version_form_set(self.request.POST, instance=self.object)
        else:
            context['formset'] = version_form_set(instance=self.object)
        return context

    def form_valid(self, form):
        version_is_active = 0
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if not self.request.user.is_superuser and not self.request.user.is_staff:
            self.object.owner = self.request.user
        self.object.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


class ProductDeleteView(PermissionRequiredMixin, generic.DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')
    permission_required = 'catalog.delete_product'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        all_product = Product.objects.all()
        context['all_product_list'] = all_product
        context['title'] = context['object']
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

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class BlogUpdateView(generic.UpdateView):
    model = Blog
    fields = ('title', 'content', 'image', 'is_published',)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        all_product = Product.objects.all()
        context['all_product_list'] = all_product
        context['title'] = context['object']
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.self()
        return super().form_valid(form)


class BlogDeleteView(generic.DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blogs')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        all_product = Product.objects.all()
        context['all_product_list'] = all_product
        context['title'] = context['object']
        return context
