import json
from .models import *


def cookieCart(request):
		try :
			cart = json.loads(request.COOKIES['cart'])
		except :
			cart = {}
		print('cart : ',cart)
		items = []                                                       # this all does not present in database just a representation of what user have and represent on screen
		order = {'get_cart_items':0, 'get_cart_total':0,'shipping':False}
		cartItems = order['get_cart_items']
		for i in cart:
		    try:
		        cartItems += cart[i]['quantity']                   #this just provide no of cart items(quantity) no items in cart same as above her_cart_items function

		        product = Product.objects.get(id=i)                #i = key of cart dict and all keys are product id
		        total = (product.price * cart[i]['quantity'])      #total price of cart items
		        order['get_cart_total'] +=total                  # set total price to drender in html
		        order['get_cart_items'] +=cart[i]['quantity']    #set total cart items value  

		        item = {
		            'product':{
		                'id':product.id,
		                'name': product.name,
		                'price': product.price,
		                'imageURL' : product.imageURL,
		                },
		            'quantity': cart[i]['quantity'],
		            'get_total':total
		            }
		        items.append(item)
		    
		        if product.digital == False:
		            order['shipping'] = True

		    except:
		        pass

		return {'items':items,'order':order,'cartItems':cartItems}


def cartData(request):
		if request.user.is_authenticated:
		    customer=request.user.customer
		    order , created = Order.objects.get_or_create(customer=customer, complete=False)  #return value is order
		    items=order.orderitem_set.all()
		    for item in items:
		    	if item.product == None:    #this is used to delete product from cart if product is not avilbale or delete from store
		    		item.delete()
		    cartItems = order.get_cart_items
		else:
		    cookiData = cookieCart(request)
		    cartItems = cookiData['cartItems']
		    order = cookiData['order']
		    items = cookiData['items']
		return {'items':items,'order':order,'cartItems':cartItems}


def guestOrder(request,data):
	print('user is not logged in..')
	print('COOKIES : ',request.COOKIES)
	name = data['form']['name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(
	    email = email,
	    )
	customer.name = name
	customer.save()

	order = Order.objects.create(
	    customer = customer,
	    complete = False 
	    )

	for item in items:
	    product = Product.objects.get(id=item['product']['id'])
	    ordetItem = OrderItem.objects.create(
	        product=product,
	        order = order,
	        quantity = item['quantity']
	        )
	return customer, order