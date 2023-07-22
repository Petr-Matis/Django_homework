from django.core.management import BaseCommand
from catalog.models import Category, Product
import json


class Command(BaseCommand):

    def handle(self, *args, **options):
        category_for_create = []
        product_for_create = []
        with open("dump_catalog.json", 'r', encoding='utf-16') as rfile:
            json_data = json.load(rfile)
            for data in json_data:
                if data['model'] == 'catalog.category':
                    category_for_create.append(Category(**data['fields']))
            Category.objects.bulk_create(category_for_create)
            for data in json_data:
                if data['model'] == 'catalog.product':
                    # Category.objects.get(pk=1)
                    product_for_create.append(Product(
                        name=data['fields']['name'],
                        description=data['fields']['description'],
                        category=Category.objects.get(pk=data['fields']['category']),
                        price=data['fields']['price'],
                        create_date=data['fields']['create_date'],
                        last_change_date=data['fields']['last_change_date'],
                    ))
            Product.objects.bulk_create(product_for_create)
