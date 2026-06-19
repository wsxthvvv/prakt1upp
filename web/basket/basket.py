from decimal import Decimal

from django.conf import settings

from bakery_app.models import Baking, Drink


class Basket:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.BASKET_SESSION_ID)
        if not cart:
            cart = self.session[settings.BASKET_SESSION_ID] = {}
        self.cart = cart

    def _product_key(self, product_type, product):
        return f'{product_type}_{product.pk}'

    def add(self, product_type, product, count=1, update_count=False):
        product_id = self._product_key(product_type, product)
        if product_id not in self.cart:
            self.cart[product_id] = {'count': 0, 'price': str(product.price)}
        if update_count:
            self.cart[product_id]['count'] = count
        else:
            self.cart[product_id]['count'] += count
        self.save()

    def remove(self, product_type, product):
        product_id = self._product_key(product_type, product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        baking_ids = []
        drink_ids = []
        for key in self.cart.keys():
            product_type, pk = key.split('_', 1)
            if product_type == 'baking':
                baking_ids.append(int(pk))
            elif product_type == 'drink':
                drink_ids.append(int(pk))

        baking_map = {f'baking_{b.pk}': b for b in Baking.objects.filter(pk__in=baking_ids)}
        drink_map = {f'drink_{d.pk}': d for d in Drink.objects.filter(pk__in=drink_ids)}

        for key, item in self.cart.items():
            product = baking_map.get(key) or drink_map.get(key)
            if not product:
                continue
            product_type = key.split('_', 1)[0]
            price = Decimal(item['price'])
            count = item['count']
            yield {
                'product': product,
                'product_type': product_type,
                'price': price,
                'count': count,
                'total_price': price * count,
            }

    def __len__(self):
        return sum(item['count'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['count'] for item in self.cart.values())

    def get_quantity(self, product_type, product):
        key = self._product_key(product_type, product)
        if key in self.cart:
            return self.cart[key]['count']
        return 0

    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        self.save()
