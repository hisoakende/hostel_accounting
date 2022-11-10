from abc import ABCMeta, abstractmethod
from typing import Union

from django.conf import settings
from django.db import models
from django.db.models.query import RawQuerySet

from goods_accounting.raw_sql_queries import all_group_purchases_query


class AbstractModelMeta(ABCMeta, type(models.Model)):
    """Метакласс, позволяющий определить абстрактные методы и при этом совместимый с django моделями"""
    pass


class AbstractModel(models.Model, metaclass=AbstractModelMeta):
    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name

    @property
    @abstractmethod
    def user_required_fields(self) -> tuple[str, ...]:
        """Обязательные к заполнению поля при передаче данных через JSON"""
        pass


class RoommatesGroupManager(models.Manager):

    def get_all_purchases(self, group: Union[int, 'RoommatesGroup']) -> RawQuerySet:
        """Метод возвращает покупки всех членов комнаты"""

        if isinstance(group, RoommatesGroup):
            group = group.pk
        return self.raw(all_group_purchases_query, (group,))


class RoommatesGroup(AbstractModel):
    """
    Модель группы человек, живущих вместе.

    Один человек может состоять в нескольких группах сразу.
    Например, у него ведется учет по группе жителей квартиры и отдельно по его комнате.
    """

    name = models.CharField('название', max_length=63)
    created_at = models.DateField('дата создания', auto_now_add=True)
    objects = RoommatesGroupManager()

    user_required_fields = ('name',)

    class Meta:
        verbose_name = 'группа человек'
        verbose_name_plural = 'группы человек'


class ProductCategory(AbstractModel):
    """Модель категории товаров. Например, продукты питания или хозяйственнные товары"""

    name = models.CharField('название', max_length=63)

    user_required_fields = ('name',)

    class Meta:
        verbose_name = 'категория продукта'
        verbose_name_plural = 'категории продуктов'


class Product(AbstractModel):
    """Модель товара. Например, молоко или изолента"""

    name = models.CharField('название', max_length=63)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='категория')

    user_required_fields = ('name', 'category')

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class Purchase(AbstractModel):
    """Модель покупки товаров"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                             verbose_name='пользователь')
    datetime = models.DateTimeField('дата и время покупки', auto_now_add=True)
    product = models.ManyToManyField(Product, through='ProductPurchase', verbose_name='продукты')

    user_required_fields = ('user', 'product')

    class Meta:
        verbose_name = 'покупка'
        verbose_name_plural = 'покупки'

    def __str__(self) -> str:
        return f'{self.user}: {self.datetime.strftime("%d.%m.%Y %H:%M:%S")}'


class ProductPurchase(AbstractModel):
    """Промежуточная таблица между моделью покупки и моделью товара"""

    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, verbose_name='покупка')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='товар')
    price = models.IntegerField('цена')

    user_required_fields = ('purchase', 'product', 'price')

    class Meta:
        verbose_name = 'покупка товара'
        verbose_name_plural = 'покупки товаров'

    def __str__(self) -> str:
        return f'{self.purchase.user}: {self.product}'
