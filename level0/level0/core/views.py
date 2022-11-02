
from coopy.base import init_persistent_system
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError


class Order:
    def __init__(self, coffee, size, milk, location, id=None):
        self.id = id
        self.coffee = coffee
        self.size = size
        self.milk = milk
        self.location = location


class CoffeeShop:
    def __init__(self):
        self.orders = {}

    def place_order(self, order):
        if order.id is None:
            order.id = len(self.orders) + 1

        self.orders[order.id] = order
        return order

coffeeshop = init_persistent_system(CoffeeShop())

def barista(request):
    """
    http://localhost:8000/PlaceOrder?coffee=latte&size=large&milk=whole&location=takeAway    
    """
    try:
        params = {k: request.GET[k]
                  for k in ('coffee', 'size', 'milk', 'location')}

    except MultiValueDictKeyError as e:
        body = 'Erro: Não foi possível registrar o pedido.'
        headers = {'Content-Type': 'text/plain; charset=utf-8'}
        return HttpResponse(body, headers=headers)

    order = Order(**params)
    coffeeshop.place_order(order)

    body = f'Order={order.id}'
    headers = {'Content-Type': 'text/plain; charset=utf-8'}

    return HttpResponse(body, headers=headers)