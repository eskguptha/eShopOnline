from django.db import models
from django.contrib.auth.models import User, Group


class Shipments(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Shipments"
        verbose_name = 'Shipments'

    def __str__(self):
        return self.name

class Products(models.Model):
    title = models.CharField(max_length=100, db_index=True, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Shipments"
        verbose_name = 'Shipments'

    def __str__(self):
        return self.title

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='customer_orders')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Shipments"
        verbose_name = 'Shipments'

    def __str__(self):
        return self.pk

class OrderProducts(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.PROTECT, related_name='customer_orders')
    product = models.ForeignKey(Products, on_delete=models.PROTECT, related_name='customer_ordered_item')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "OrderProducts"
        verbose_name = 'OrderProducts'

    def __str__(self):
        return self.pk

class OrderShipments(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.PROTECT,related_name='orders_shipments')
    shipment = models.ForeignKey(Shipments, on_delete=models.PROTECT, related_name='Shipment_Vendor')
    shipment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "OrderShipments"
        verbose_name = 'OrderShipments'

    def __str__(self):
        return self.pk

