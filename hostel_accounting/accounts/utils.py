from typing import Union

from rest_framework.request import Request
from rest_framework.response import Response

from accounts.models import RoommatesGroup, User
from goods_accounting.models import ProductCategory, Product, ProductPurchase, Purchase
from hostel_accounting.serializers import AllGroupsPurchasesSerializer
from hostel_accounting.utils import get_all_fields_from_request


def process_raw_groups_purchases(pk: int) -> list[dict[str, Union[User, list[ProductPurchase]]]]:
    """Функция, обрабатывающая сырые данные всех покупок группы для дальнейшей сериализации"""

    users_id = []
    users_purchases = []
    for obj in RoommatesGroup.objects.get_all_purchases(pk):
        if obj.user_id not in users_id:
            users_purchases.append(
                {'user': User(pk=obj.user_id, username=obj.username, email=obj.email, first_name=obj.first_name,
                              last_name=obj.last_name, is_superuser=obj.is_superuser, is_staff=obj.is_staff,
                              date_joined=obj.date_joined, last_login=obj.last_login), 'products': []}
            )
            users_id.append(obj.user_id)
        index = users_id.index(obj.user_id)

        category = ProductCategory(pk=obj.category_id, name=obj.category_name)
        product = Product(pk=obj.product_id, name=obj.product_name, category=category)
        product_purchase = ProductPurchase(purchase=Purchase(), product=product, price=obj.price)

        users_purchases[index]['products'].append(product_purchase)
    return users_purchases


def get_response_while_processing_groups_purchases(request: Request, roommates_group: RoommatesGroup) -> Response:
    """Функция, возращающая ответ на запрос получения всех покупок комнаты"""

    raw_data = {'roommates_group': roommates_group,
                'users_purchases': process_raw_groups_purchases(int(roommates_group.pk))}

    fields_params = get_all_fields_from_request(request, ('fields', 'roommates_group_fields', 'user_fields',
                                                          'product_fields', 'product_category_fields'))
    serializer = AllGroupsPurchasesSerializer(raw_data, **fields_params)
    return Response(serializer.data)
