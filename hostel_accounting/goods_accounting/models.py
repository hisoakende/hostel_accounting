from typing import Union

from django.conf import settings
from django.db import models
from django.db.models.query import RawQuerySet

from goods_accounting.raw_sql_queries import all_group_purchases_query


class StrMethodMixin:

    def __str__(self) -> str:
        return self.name


class RoommatesGroupManager(models.Manager):

    def get_all_purchases(self, group: Union[int, 'RoommatesGroup']) -> RawQuerySet:
        """Метод возвращает покупки всех членов комнаты"""

        if isinstance(group, RoommatesGroup):
            group = group.pk
        return self.raw(all_group_purchases_query, (group,))


class RoommatesGroup(StrMethodMixin, models.Model):
    """Модель группы человек, живущих вместе"""

    name = models.CharField('название', max_length=63)
    created_at = models.DateField('дата создания', auto_now_add=True)
    objects = RoommatesGroupManager()

    class Meta:
        verbose_name = 'группа человек'
        verbose_name_plural = 'группы человек'


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
    product = models.ManyToManyField(Product, through='ProductPurchase', verbose_name='продукты')

    class Meta:
        verbose_name = 'покупка'
        verbose_name_plural = 'покупки'

    def __str__(self) -> str:
        return f'{self.user}: {self.datetime.strftime("%d.%m.%Y %H:%M:%S")}'


class ProductPurchase(models.Model):
    """Промежуточная таблица между моделью покупки и моделью товара"""

    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, verbose_name='покупка')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='товар')
    price = models.IntegerField('цена')

    class Meta:
        verbose_name = 'покупка товара'
        verbose_name_plural = 'покупки товаров'

    def __str__(self) -> str:
        return f'{self.purchase.user}: {self.product}'
