from django.contrib import admin
from .models import *

admin.site.register(LaboratoryItem)
admin.site.register(LaboratoryOrder)
admin.site.register(LaboratoryOrderItems)
# Register your models here.