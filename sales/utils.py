import json

from accounts.models import User
from . models import *

def cookieCart(request):
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        print('cart: ',cart)
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

        for i in cart:
            ''' Handles any errors when the item present in cart cookie
                has been removed from the database.
                The best way is to inform the user that the item is no longer
                available.
            '''
            try: 
                cartItems += cart[i]['quantity']

                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'price':product.price,
                        'imageURL':product.imageURL,
                    },
                    'quantity':cart[i]["quantity"],
                    'get_total':total
                }

                items.append(item)

                if product.digital == False:
                    order['shipping'] = True
            except:
                 pass

        return {'items':items, 'order':order, 'cartItems': cartItems}


def cartData(request):
    if request.user.is_authenticated:
        user = request.user

        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Handle guest user
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'items':items, 'order':order, 'cartItems': cartItems}


def guestOrder(request, data):

    print("User is not logged in...")

    print('COOKIES', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    user, created = User.objects.get_or_create(
        email = email,
    )

    user.name = name
    user.save()

    order = Order.objects.create(
        customer =user,
        complete = False,             
    )

    for item in items:
        product = Product.objects.get(id=item["product"]['id'])

        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity']
        )

    return user, order