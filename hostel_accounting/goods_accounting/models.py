from django.conf import settings
from django.db import models


class NameStrMixin:
    name = None

    def __str__(self) -> str:
        return self.name


class RoommatesGroup(NameStrMixin, models.Model):
    """
    Модель группы человек, живущих вместе.

    Один человек может состоять в нескольких группах сразу.
    Например, у него ведется учет по группе жителей квартиры и отдельно по его комнате.
    """

    name = models.CharField('название', max_length=63)
    created_at = models.DateField('дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'группа человек'
        verbose_name_plural = 'группы человек'


class ProductCategory(NameStrMixin, models.Model):
    """Модель категории товаров. Например, продукты питания или хозяйственнные товары"""

    name = models.CharField('название', max_length=63)

    class Meta:
        verbose_name = 'категория продукта'
        verbose_name_plural = 'категории продуктов'


class Product(NameStrMixin, models.Model):
    """Модель товара. Например, молоко или изолента"""

    name = models.CharField('название', max_length=63)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='категория')

    class Meta:
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
