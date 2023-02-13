from django.db import models
from django.db.models import F, Sum
from django.core.validators import MinValueValidator
# from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.modelfields import PhoneNumberField

import datetime


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


# class OrderQuerySet(models.QuerySet):
#     def cost(self):
#         # cost_item = self.order_items.all().annotate(order_cost=F('product__price')*F('quantity'))
#         # cost_item = self.annotate(order_cost=F('order_items__product__price')*F('order_items__quantity'))
#         cost = self.aggregate(cost=Sum(self.annotate(order_cost=F('order_items__product__price')*F('order_items__quantity'))))
#         return cost['cost']
#         # return cost_item.aggregate(cost=Sum('order_cost'))


# class OrderManager(models.Manager):
#     def get_queryset(self):
#         return OrderQuerySet(self.model)
    
#     def cost(self):
#         return self.get_queryset().cost()


class Order(models.Model):
    PROCESSING = 'необработанный'
    ASSEMLY = 'сборка'
    DELIVERY = 'доставка'
    FINISHED = 'исполнен'
    STATUS_CHOICES = [
        (PROCESSING, 'необработанный'),
        (ASSEMLY, 'сборка'),
        (DELIVERY, 'доставка'),
        (FINISHED, 'исполнен'),
    ]
    firstname = models.CharField(
        'Имя',
        max_length=50
    )
    lastname = models.CharField(
        'Фамилия',
        max_length=50
    )
    phonenumber = PhoneNumberField()
    address = models.CharField(
        'адрес',
        max_length=100,
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default=PROCESSING,
        db_index=True,
        verbose_name='статус заказа'
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        default='',
        null=True,
        blank=True
    )
    regisred_at = models.DateTimeField(
        verbose_name='Время регистрации',
        db_index=True,
        default=datetime.datetime.now
    )
    called_at = models.DateTimeField(
        verbose_name='Время звонка',
        null=True,
        blank=True
    )
    delivered_at = models.DateTimeField(
        verbose_name='Время доставки',
        null=True,
        blank=True
    )
    # objects = OrderQuerySet.as_manager()
    # objects = models.Manager()
    # order_cost = OrderManager()
    # order_cost = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Заказ {self.id} - для {self.phonenumber}'


class OrderMenuItem(models.Model):    
    order = models.ForeignKey(
        Order,
        related_name='order_items',
        verbose_name="заказ",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='продукт',
    )
    price = models.DecimalField(
        'цена',
        validators=[MinValueValidator(0)],
        max_digits=8,
        default=0,
        decimal_places=2,
    )
    quantity = models.IntegerField(
        'количество',
        default=1,
        db_index=True
    )
    

    class Meta:
        verbose_name = 'пункт заказа'
        verbose_name_plural = 'пункты заказа'
        unique_together = [
            ['order', 'product']
        ]
