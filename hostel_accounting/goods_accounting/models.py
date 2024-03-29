from django.conf import settings
from django.db import models

from hostel_accounting.utils import StrMethodMixin


class ProductCategory(StrMethodMixin, models.Model):
    """Модель категории товаров. Например, продукты питания или хозяйственнные товары"""

    name = models.CharField('название', max_length=63)

    class Meta:
        verbose_name = 'категория продукта'
        verbose_name_plural = 'категории продуктов'


class Product(StrMethodMixin, models.Model):
    """Модель товара. Например, молоко или изолента"""

    name = models.CharField('название', max_length=63)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='категория')

    class Meta:
        ordering = ('id',)
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class Purchase(models.Model):
    """Модель покупки товаров"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                             verbose_name='пользователь')
    datetime = models.DateTimeField('дата и время покупки', auto_now_add=True)
    products = models.ManyToManyField(Product, through='ProductPurchase', verbose_name='продукты')

    class Meta:
        ordering = ('id',)
        verbose_name = 'покупка'
        verbose_name_plural = 'покупки'

    def __str__(self) -> str:
        return f'{self.user}: {self.datetime.strftime("%d.%m.%Y %H:%M:%S")}'


class ProductPurchase(models.Model):
    """Промежуточная таблица между моделью покпки и моделью товара"""

    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, verbose_name='покупка')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='товар')
    price = models.IntegerField('цена')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'покупка товара'
        verbose_name_plural = 'покупки товаров'

    def __str__(self) -> str:
        return f'{self.purchase.user}: {self.product} ({self.price})'
