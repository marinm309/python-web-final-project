from products.models import Order

def CartMiddleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        user = request.user
        if user.is_authenticated:
            order, created = Order.objects.get_or_create(customer=user.customer, completed=False)
            items = order.orderitem_set.all()
            total_cart_items = sum(map(lambda x :x.quantity, items))
            request.cart_items = total_cart_items
        else:
            print(123456789)

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware