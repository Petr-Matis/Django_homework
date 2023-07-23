from django.shortcuts import render

from catalog.models import Product, Category
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage



def catalog(request):
    products_list = Product.objects.all().order_by('id')
    paginator = Paginator(products_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'object_list': products_list,
        'page_object': page_obj,
        'title': 'Главное меню "Каталог"'
    }
    return render(request, 'catalog/index.html', context)


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


def product(request, pk):
    products_list = Product.objects.all()
    product_item = Product.objects.get(pk=pk)
    context = {
        'object_list': products_list,
        'product': product_item,
        'title': f'Товар {product_item.name}'
    }
    return render(request, 'catalog/product.html', context=context)


def add_product(request):
    products_list = Product.objects.all()
    category_list = Category.objects.all()
    context = {
        'object_list': products_list,
        'category_list': category_list,
        'add_items': None,
        'title': f'Добавить товар',
    }
    if request.method == 'POST':
        product_item = Product(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            category=Category.objects.get(name=request.POST.get('category')),
            price=request.POST.get('price'))
        if request.POST.get('image') != '':
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(f'products/{image.name}', image)
            uploaded_file_url = fs.url(filename)
            product_item.image = filename
        product_item.save()
        context['add_items'] = True
    return render(request, 'catalog/add_product.html', context=context)
