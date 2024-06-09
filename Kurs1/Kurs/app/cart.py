from decimal import Decimal
from django.conf import settings
from django.apps import apps


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity}
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def get_quantity(self, product_id):
        product_id = str(product_id)
        return self.cart.get(product_id, {}).get('quantity', 0)

    def save(self):
        self.session.modified = True

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        Product = apps.get_model('app', 'Product')  # Используйте отложенную загрузку
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            cart_item = self.cart[str(product.id)]
            cart_item['product'] = product

            # Расчет цены с учетом скидки
            if product.discount:
                cart_item['price'] = Decimal(product.price) * (1 - Decimal(product.discount) / 100)
            else:
                cart_item['price'] = Decimal(product.price)

            cart_item['total_price'] = cart_item['price'] * cart_item['quantity']
            yield cart_item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        total_price = 0
        for item in self:  # Используем итератор для перебора товаров с учетом скидок
            total_price += item['total_price']
        return total_price

    def decrement(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= 1
            if self.cart[product_id]['quantity'] == 0:
                del self.cart[product_id]
            self.save()

    def increment(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += 1
            self.save()