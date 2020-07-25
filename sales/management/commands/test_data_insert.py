from django.core.management.base import BaseCommand
import random
from datetime import datetime
from sales.models import User, Shipments, Products, Orders, OrderProducts, OrderShipments
import traceback

class Command(BaseCommand):
    help = 'Test Data Insert'

    def handle(self, *args, **options):


        try:
            Shipments.objects.create(name="shipments_1")
        except Shipments.DoesNotExist:
            traceback.print_exc()
            pass

        no_of_products = 5
        for i in range(no_of_products):
            try:
                product_obj = Products.objects.create(title="item_{}".format(i), price=random.uniform(10.01, 99.99))
            except Products.DoesNotExist:
                traceback.print_exc()
                pass