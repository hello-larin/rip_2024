from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(LaboratoryItem)
admin.site.register(LaboratoryOrder)
admin.site.register(LaboratoryOrderItems)