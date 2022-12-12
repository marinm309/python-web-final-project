from products.models import Order
import json

def CartMiddleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        user = request.user
        if user.is_authenticated:
            order, created = Order.objects.get_or_create(customer=user.customer, completed=False)
            items = order.orderitem_set.all()
            total_cart_items = sum(map(lambda x :x.quantity, items))
        else:
            try:
                cart = json.loads(request.COOKIES['cart'])
            except:
                cart = {}

            total_cart_items = 0
        
            for i in cart:
                total_cart_items += cart[i]['quantity']
        
        request.cart_items = total_cart_items

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware

def UserCookieMiddleware(get_response):

    def middleware(request):
        user = request.user

        response = get_response(request)

        response.set_cookie('user', user)

        return response

    return middleware