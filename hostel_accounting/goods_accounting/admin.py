from django.contrib import admin

from .models import *


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ('name', 'category')
    list_display = ('name', 'category')


class ProductInline(admin.TabularInline):
    model = Purchase.products.through
    can_delete = False
    extra = 0


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    fields = ('user', 'datetime')
    readonly_fields = ('datetime',)
    list_display = ('user', 'datetime')
    inlines = (ProductInline,)
