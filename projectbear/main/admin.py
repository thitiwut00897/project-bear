from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import *
# Register your models here.
admin.site.register(Product)
admin.site.register(Type)
admin.site.register(Profile)
admin.site.register(Permission)
