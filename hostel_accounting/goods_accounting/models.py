from django.conf import settings
from django.db import models


class RoommatesGroup(models.Model):
    """
    Модель группы человек, живущих вместе.

    Один человек может состоять в нескольких группах сразу.
    Например, у него ведется учет по группе жителей квартиры и отдельно по его комнате.
    """

    name = models.CharField('название', max_length=63)
    created_at = models.DateField('дата создания', auto_now_add=True)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='пользователи')

    def __str__(self) -> str:
        return f'Группа: {self.name}'


class ProductCategory(models.Model):
    """Модель категории товаров. Например, продукты питания или хозяйственнные товары"""

    name = models.CharField('название', max_length=63)

    def __str__(self) -> str:
        return f'Категория: {self.name}'


class Product(models.Model):
    """Модель товара. Например, молоко или изолента"""

    name = models.CharField('название', max_length=63)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='категория')

    def __str__(self) -> str:
        return f'Продукт: {self.name}'


class Purchase(models.Model):
    """Модель покупки товаров"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                             verbose_name='пользователь')
    datetime = models.DateTimeField('дата и время покупки', auto_now_add=True)
    product = models.ManyToManyField(Product, through='ProductPurchase', verbose_name='продукты')

    def __str__(self) -> str:
        return f'Покупка: {self.user.username if self.user is not None else "<Аноним>"}, дата и время: {self.datetime}'


class ProductPurchase(models.Model):
    """Промежуточная таблица между моделью покупки и моделью товара"""

    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, verbose_name='покупка')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='товар')
    price = models.IntegerField('цена')

    def __str__(self) -> str:
        return f'Покупка товара: {self.product.name if self.product is not None else "<удален>"}, цена: {self.price}'
