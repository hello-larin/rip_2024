# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

#class CustomUser(AbstractBaseUser, PermissionsMixin):
#    username =  models.CharField(("Логин"), unique=True, max_length=150)
#    password = models.CharField(max_length=50, verbose_name="Пароль")    
#    is_staff = models.BooleanField(default=False, verbose_name="Является ли пользователь менеджером?")
#    is_superuser = models.BooleanField(default=False, verbose_name="Является ли пользователь админом?")

class LaboratoryItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    image = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=1)

    class Meta:
        db_table = 'laboratory_item'


class LaboratoryOrder(models.Model):
    id = models.BigAutoField(primary_key=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    accepted_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    status = models.IntegerField()
    submited_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=False, related_name='creator')
    moderator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='moderator_name')
    delivery_number = models.CharField(max_length=16, blank=True, null=True)


    class Meta:
        db_table = 'laboratory_order'


class LaboratoryOrderItems(models.Model):
    id = models.BigAutoField(primary_key=True)
    amount = models.IntegerField()
    order = models.ForeignKey(LaboratoryOrder, models.DO_NOTHING, related_name='equipment')
    product_id = models.ForeignKey(LaboratoryItem, models.DO_NOTHING, related_name='equipment')

    class Meta:
        db_table = 'laboratory_order_items'
        unique_together = ('order', 'product_id')