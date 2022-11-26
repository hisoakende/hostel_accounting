from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

id_path_parameter = OpenApiParameter(
    'id',
    type=OpenApiTypes.INT,
    location=OpenApiParameter.PATH
)

page_param_ru = OpenApiParameter(
    'page',
    type=OpenApiTypes.INT,
    location=OpenApiParameter.QUERY,
    description='Номер страницы в наборе результатов с разбивкой на страницы'
)

page_size_param_ru = OpenApiParameter(
    'page_size',
    type=OpenApiTypes.INT,
    location=OpenApiParameter.QUERY,
    description='Количество записей на одной странице'
)
