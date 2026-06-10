from django.db import models
from django.contrib.auth.models import User

MAX_LENGTH = 255

class Category(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Baking(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    weight = models.PositiveIntegerField(null=True, blank=True, verbose_name='Вес (г)')
    diameter = models.PositiveIntegerField(null=True, blank=True, verbose_name='Диаметр (см)')
    filling = models.CharField(max_length=MAX_LENGTH, verbose_name='Начинка', default='')
    photo = models.ImageField(upload_to='image/%Y/%m/%d', null=True, blank=True, verbose_name='Изображение')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления на сайт')
    is_exists = models.BooleanField(default=True, verbose_name='Доступность к заказу')

    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"

    class Meta:
        verbose_name = 'Выпечка'
        verbose_name_plural = 'Выпечка'

class Drink(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    volume = models.PositiveIntegerField(null=True, blank=True, verbose_name='Объём (мл)')
    photo = models.ImageField(upload_to='image/%Y/%m/%d', null=True, blank=True, verbose_name='Изображение')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления на сайт')
    is_exists = models.BooleanField(default=True, verbose_name='Доступность к заказу')

    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Напиток'
        verbose_name_plural = 'Напитки'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Телефон')
    address = models.TextField(null=True, blank=True, verbose_name='Адрес')
    photo = models.ImageField(upload_to='profiles/%Y/%m/%d', null=True, blank=True, verbose_name='Изображение')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class Review(models.Model):
    author_name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование')
    text = models.TextField(verbose_name='Описание')
    rating = models.PositiveIntegerField(default=5, verbose_name='Оценка')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления на сайт')
    baking = models.ForeignKey(Baking, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Выпечка')
    drink = models.ForeignKey(Drink, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Напиток')

    def __str__(self):
        return self.author_name

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class Order(models.Model):
    customer_name = models.CharField(max_length=MAX_LENGTH, verbose_name='Имя клиента')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.TextField(verbose_name='Адрес доставки')
    delivery = models.ForeignKey('Delivery', on_delete=models.PROTECT, verbose_name='Зона доставки')
    status = models.CharField(max_length=MAX_LENGTH, default='новый', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')

    def __str__(self):
        return self.customer_name

    def get_total(self):
        total = 0
        for item in self.items.all():
            if item.baking:
                total += item.baking.price * item.quantity
            elif item.drink:
                total += item.drink.price * item.quantity
        return total

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    baking = models.ForeignKey(Baking, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Выпечка')
    drink = models.ForeignKey(Drink, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Напиток')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        if self.baking:
            return f'{self.baking.name} × {self.quantity}'
        if self.drink:
            return f'{self.drink.name} × {self.quantity}'
        return f'Позиция #{self.pk}'

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

class Delivery(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(verbose_name='Стоимость доставки')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставка'

class Promotion(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    discount = models.FloatField(verbose_name='Скидка (%)')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'
