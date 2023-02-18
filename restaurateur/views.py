from django import forms
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views

from django.db.models import F, Sum

import requests
from geopy import distance

from foodcartapp.models import Product, Restaurant, Order, RestaurantMenuItem
from star_burger.settings import YANDEX_MAP_API


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


def get_restaurants(query_set):
    restaurants = []
    order_items = query_set.order_items.all()
    if len(order_items) == 0:
        return restaurants
    elif len(order_items) == 1:
        for order_item in order_items:
            menu_items = order_item.product.menu_items.all()
            for menu_item in menu_items:
                restaurants.append(menu_item.restaurant)
        return restaurants
    else:
        for order_item in order_items:
            all_restaurants = []
            temp_restaurants = []
            menu_items = order_item.product.menu_items.all()
            for menu_item in menu_items:
                temp_restaurants.append(menu_item.restaurant)
            all_restaurants.append(temp_restaurants)
            restaurants = list(set.intersection(*map(set, all_restaurants)))
        return restaurants


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    # return lon, lat
    return lat, lon


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    restaurants_distance = {}
    order_items = Order.objects.exclude(status='исполнен').all()
    for item in order_items:
        cost_item = item.order_items.all().annotate(order_cost=F('price')*F('quantity'))
        cost = cost_item.aggregate(cost=Sum('order_cost'))
        item.cost = cost['cost']
        item.change_url = reverse('admin:foodcartapp_order_change', args =(item.id, ))
        if not item.restaurant:
            item.all_restaurants = get_restaurants(item)
            item_distances = []
            for restaurant in item.all_restaurants:
                # print(restaurant)
                # try:
                #     client_coord = fetch_coordinates(YANDEX_MAP_API, item.address)
                #     restaurant_coord = fetch_coordinates(YANDEX_MAP_API, restaurant.address)
                #     item_distances.append({restaurant.name: distance.distance(client_coord, restaurant_coord).km})
                # except:
                #     item_distances.append({restaurant.name: 'Не удалость расчитать растояние'})
                item_distances.append({restaurant.name: restaurant.address})
            restaurants_distance[item.id] = item_distances
        # else:
        #     try:
        #         client_coord = fetch_coordinates(YANDEX_MAP_API, item.address)
        #         restaurant_coord = fetch_coordinates(YANDEX_MAP_API, item.restaurant.address)
        #         distance_km = distance.distance(client_coord, restaurant_coord).km
        #     except:
        #         print('Не удалость расчитать растояние')
            
    # print(restaurants_distance[29])
    # for item in restaurants_distance:
    #     print(type(item))
    #     # for temp_item in restaurants_distance[item]:
    #     #     for i, y in temp_item.items():
    #     #         print(i, y)
    
    return render(request, template_name='order_items.html', context={
        'order_items': order_items,
        'restaurants_distance': restaurants_distance,
    })
