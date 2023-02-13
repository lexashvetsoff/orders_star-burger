from django.http import JsonResponse
from django.templatetags.static import static

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from .serializer import FoodcartappSerializer

from .models import Product
from .models import Order
from .models import OrderMenuItem


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    data = request.data

    serializer = FoodcartappSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    
    # order_sum = 0
    order = Order.objects.create(
        firstname = serializer.validated_data['firstname'],
        lastname = serializer.validated_data['lastname'],
        phonenumber = serializer.validated_data['phonenumber'],
        address = serializer.validated_data['address'],
    )

    for product in serializer.validated_data['products']:
        order_product = Product.objects.get(id=product['product'].id)
        # sum = order_product.price * product['quantity']
        # order_sum += sum

        OrderMenuItem.objects.create(
            order = order,
            product = order_product,
            quantity = product['quantity'],
            sum = sum,
        )
    # order.sum = order_sum
    order.save()
    content = JSONRenderer().render(serializer.data)
    print(content)
    # return JsonResponse({content}, safe=False)
    return Response(content)
