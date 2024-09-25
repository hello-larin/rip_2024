from django.db import models

# Create your models here.

class LaboratoryItem(models.Model):
    name = models.CharField(max_length=255)  # Название продукта
    description = models.TextField(blank=True)  # Описание продукта
    price = models.IntegerField()  # Цена продукта
    image = models.TextField() # URL изображения продукта

    class Meta:
        db_table = 'laboratory_item'


class LaboratoryOrder(models.Model):
    address = models.TextField(blank=True)  # Адрес доставки
    phone = models.CharField(max_length=15, blank=True)  # Номер телефона

    class Meta:
        db_table = 'laboratory_order'


class LaboratoryOrderItems(models.Model):
    order = models.ForeignKey(LaboratoryOrder, on_delete=models.CASCADE)  # Связь с заказом
    product_id = models.ForeignKey(LaboratoryItem, on_delete=models.CASCADE)
    amount = models.IntegerField()  # Количество товара

    class Meta:
        db_table = 'laboratory_order_items'

