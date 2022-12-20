from typing import Callable, Union, Literal

from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import ValidationError, ErrorDetail
from rest_framework.request import Request
from rest_framework.response import Response

from goods_accounting.api.serializers import ProductPurchaseSerializer, PurchaseSerializer
from goods_accounting.models import ProductPurchase, Purchase, Product
from utils import get_obj_by_pk


def add_product_to_purchase(purchase: Purchase, product: Product, price: int, errors: list) -> None:
    """Функция, добавляющая продукт в покупку"""

    ProductPurchase.objects.create(purchase=purchase, product=product, price=price)


def delete_product_from_purchase(purchase: Purchase, product: Product, price: int, errors: list) -> None:
    """Функция, удаляющая продукт из покупки"""

    products_purchase = ProductPurchase.objects.filter(purchase=purchase, product=product, price=price)
    if len(products_purchase) == 0:
        errors.append(f'Покупки товара c такими данными {purchase.pk, product.id, price} не существует')
    else:
        products_purchase[0].delete()


def process_deletion_or_addition_product_purchase(purchase: Purchase, validated_data: list[tuple[Product, int]],
                                                  errors: list, func: Callable) -> None:
    """Функция, обрабатывающая удаление или добавление продуктов в/из покупки"""

    with transaction.atomic():
        for product, price in validated_data:
            func(purchase, product, price, errors)


def process_errors(errors: Union[dict[str, ErrorDetail], list[ErrorDetail]]) -> list[str]:
    """
    Функция, переводящая ошибки при обработке добавления/удаления
    продукта в покупку в удобный для ответа формат
    """

    if isinstance(errors, dict):
        errors = errors.values()
    return sum(filter(lambda e: e, errors), [])


def process_deletion_or_addition_product_purchase_request(request: Request, pk: str,
                                                          func: Callable, response_code: Literal[200, 204]) -> Response:
    """Функция, обрабатывающая запрос на удаление или для добавление продуктов в покупку"""

    if not pk.isdigit():
        return Response({'errors': ['Такой покупки не существует']},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        purchase = get_obj_by_pk(Purchase, int(pk))
    except ValidationError:
        return Response({'errors': ['Такой покупки не существует']},
                        status=status.HTTP_400_BAD_REQUEST)

    product_purchase_data = ProductPurchaseSerializer(data=request.data, validate_by_id=True, many=True)
    if not product_purchase_data.is_valid():
        errors = process_errors(product_purchase_data._errors)
        return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

    errors = []
    process_deletion_or_addition_product_purchase(purchase, product_purchase_data.validated_data, errors, func)
    if errors:
        return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

    if response_code == 204:
        return Response(status=status.HTTP_204_NO_CONTENT)

    purchase.refresh_from_db()
    serializer = PurchaseSerializer(purchase)
    return Response(serializer.data)
