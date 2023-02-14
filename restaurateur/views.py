from django import forms
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views

from django.db.models import F, Sum


from foodcartapp.models import Product, Restaurant, Order, RestaurantMenuItem


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


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):

    order_items = Order.objects.exclude(status='исполнен').all()
    for item in order_items:
        cost_item = item.order_items.all().annotate(order_cost=F('price')*F('quantity'))
        cost = cost_item.aggregate(cost=Sum('order_cost'))
        item.cost = cost['cost']
        item.change_url = reverse('admin:foodcartapp_order_change', args =(item.id, ))
        if not item.restaurant:
            item.all_restaurants = get_restaurants(item)
        print(item.restaurant)
    
    # print(order_items[35].order_items.all()[0].product.menu_items.all()[0].restaurant)
    
    return render(request, template_name='order_items.html', context={
        'order_items': order_items,
    })
