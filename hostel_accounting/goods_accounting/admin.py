from django.contrib import admin

from accounts.admin import UserInline
from .models import *


@admin.register(RoommatesGroup)
class RoommatesGroupAdmin(admin.ModelAdmin):
    fields = ('name', 'created_at')
    readonly_fields = ('created_at',)
    list_display = ('name', 'created_at')
    inlines = (UserInline,)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ('name', 'category')
    list_display = ('name', 'category')


class ProductInline(admin.TabularInline):
    model = Purchase.product.through
    can_delete = False
    extra = 0


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    fields = ('user', 'datetime')
    readonly_fields = ('datetime',)
    list_display = ('user', 'datetime')
    inlines = (ProductInline,)


@admin.register(ProductPurchase)
class ProductPurchaseAdmin(admin.ModelAdmin):
    fields = ('purchase', 'product', 'price')
    list_display = ('purchase', 'product', 'price')
