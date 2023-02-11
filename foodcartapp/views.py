from django.http import JsonResponse
from django.templatetags.static import static

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

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

    # if not 'products' in data:
    #     content = {
    #         'error': 'products: Обязательное поле.',
    #     }
    #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # if (not 'firstname' in data and
    #     not 'lastname' in data and
    #     not 'phonenumber' in data and
    #     not 'address' in data):
    #     content = {
    #         'error': 'firstname, lastname, phonenumber, address: Обязательное поле.',
    #     }
    #     return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # if isinstance(data['products'], type(None)):
    #     content = {
    #         'error': 'products: Это поле не может быть пустым.',
    #     }
    #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # if (isinstance(data['firstname'], type(None)) and
    #     isinstance(data['lastname'], type(None)) and
    #     isinstance(data['phonenumber'], type(None)) and
    #     isinstance(data['address'], type(None))):
    #     content = {
    #         'error': 'firstname, lastname, phonenumber, address: Это поле не может быть пустым.',
    #     }
    #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # if isinstance(data['firstname'], type(None)):
    #     content = {
    #         'error': 'firstname: Это поле не может быть пустым.',
    #     }
    #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # if isinstance(data['lastname'], type(None)):
    #     content = {
    #         'error': 'lastname: Это поле не может быть пустым.',
    #     }
    #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # if isinstance(data['phonenumber'], type(None)):
    #     content = {
    #         'error': 'phonenumber: Это поле не может быть пустым.',
    #     }
    #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # if isinstance(data['address'], type(None)):
    #     content = {
    #         'error': 'address: Это поле не может быть пустым.',
    #     }
    #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # if not isinstance(data['products'], list):
    #     content = {
    #         'error': 'products: Ожидался list со значениями, но был получен "str".',
    #     }
    #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
    # elif len(data['products']) == 0:
    #     content = {
    #         'error': 'products: Этот список не может быть пустым.',
    #     }
    #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # if not data['firstname']:
    #     content = {
    #         'error': 'firstname: Это поле не может быть пустым.',
    #     }
    #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # if not data['lastname']:
    #     content = {
    #         'error': 'lastname: Это поле не может быть пустым.',
    #     }
    #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # if not data['phonenumber']:
    #     content = {
    #         'error': 'phonenumber: Это поле не может быть пустым.',
    #     }
    #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # if not data['address']:
    #     content = {
    #         'error': 'address: Это поле не может быть пустым.',
    #     }
    #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # if isinstance(data['firstname'], list):
    #     content = {
    #         'error': 'В поле firstname положили список.',
    #     }
    #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # if isinstance(data['lastname'], list):
    #     content = {
    #         'error': 'В поле lastname положили список.',
    #     }
    #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # if isinstance(data['phonenumber'], list):
    #     content = {
    #         'error': 'В поле phonenumber положили список.',
    #     }
    #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # if isinstance(data['address'], list):
    #     content = {
    #         'error': 'В поле address положили список.',
    #     }
    #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # for product in data['products']:
    #     if not Product.objects.filter(id=product['product']).exists():
    #         id = product['product']
    #         content = {
    #         'error': f'products: Недопустимый первичный ключ "{id}".',
    #     }
    #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
    # {"products": [{"product": 1, "quantity": 1}], "firstname": "Иван", "lastname": "Петров", "phonenumber": "+79291000000", "address": "Москва"}

    
    order_sum = 0
    order = Order.objects.create(
        firstname = serializer.validated_data['firstname'],
        lastname = serializer.validated_data['lastname'],
        phonenumber = serializer.validated_data['phonenumber'],
        address = serializer.validated_data['address'],
    )
    # print(order.id)
    # print(serializer.validated_data['products'])
    # exit()
    for product in serializer.validated_data['products']:
        # print(product['product'])
        # exit()
        order_product = Product.objects.get(id=product['product'].id)
        sum = order_product.price * product['quantity']
        order_sum += sum

        OrderMenuItem.objects.create(
            order = order,
            product = order_product,
            quantity = product['quantity'],
            sum = sum,
        )
    order.sum = order_sum
    order.save()
    return JsonResponse({})
