import json
from . models import Products, Order

def guest_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    total_items = 0
    total_price = 0
        
    for i in cart:
        try:
            total_items += cart[i]['quantity']
            product = Products.objects.get(pk=i)
            total_price += product.price * cart[i]['quantity']
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'img': product.img
                },
                'quantity': cart[i]['quantity'],
            }
            items.append(item)
        except:
            pass
    return {'total_items': total_items, 'total_price': total_price, 'items': items}


def cart_details(request):
    order = ''
    customer = ''
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        total_items = sum(map(lambda x :x.quantity, items))
        total_price = sum(map(lambda x :x.product.price * x.quantity, items))
    else:
        context_data = guest_cart(request)
        items = context_data['items']
        total_items = context_data['total_items']
        total_price = context_data['total_price']
    
    return {'total_items': total_items, 'total_price': total_price, 'items': items, 'order': order, 'customer': customer}