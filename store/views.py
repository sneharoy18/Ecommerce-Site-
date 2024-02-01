from django.shortcuts import render, redirect

from django.http import JsonResponse
import json

import datetime

from .models import *

from .utils import cookieCart, cartData, guestOrder

from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .decorators import unauthenticated_user,allowed_user
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group

from .filters import OrderFilter
# Create your views here.

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    '''if request.user.is_authenticated:
                    customer = request.user.customer
                    order, created = Order.objects.get_or_create(customer=customer, complete=False)
                    items = order.orderitem_set.all()
                    cartItems = order.get_cart_items
        #Create empty cart for now for non-logged in user
                                items = []
                                order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
                                cartItems = order['get_cart_items']
                        '''
                
    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def viewProduct(request,pk):
    data = cartData(request)
    cartItems = data['cartItems']

    product = Product.objects.get(id=pk)
    detail = ProductDetail.objects.get(product=product)
    context = {'product':product,'cartItems':cartItems,'detail':detail}
    return render(request,'store/viewProduct.html',context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    '''if request.user.is_authenticated:
                    customer = request.user.customer
                    order, created = Order.objects.get_or_create(customer=customer, complete=False)
                    items = order.orderitem_set.all()
                    cartItems = order.get_cart_items

        #Create empty cart for now for non-logged in user
                                try:
                                    cart = json.loads(request.COOKIES['cart'])
                                except:
                                    cart = {}
                                    print('CART:', cart)
                        
                                items = []
                                order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
                                cartItems = order['get_cart_items']
                        
                                for i in cart:
                                    try:
                                        cartItems += cart[i]['quantity']
                                        product = Product.objects.get(id=i)
                                        total = (product.price * cart[i]['quantity'])
                        
                                        order['get_cart_total'] += total
                                        order['get_cart_items'] += cart[i]['quantity']
                        
                                        item = {
                                            'id':product.id,
                                            'product':{'id':product.id,'name':product.name, 'price':product.price, 
                                            'imageURL':product.imageURL}, 'quantity':cart[i]['quantity'],
                                            'digital':product.digital,'get_total':total,
                                            }
                                        items.append(item)
                        
                                        if product.digital == False:
                                            order['shipping'] = True
                                    except:
                                        pass'''

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

  
@csrf_exempt
def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/checkout.html',context)
    
    '''if request.user.is_authenticated:
                    customer = request.user.customer


                    order, created = Order.objects.get_or_create(customer=customer, complete=False)
                    items = order.orderitem_set.all()
                    cartItems = order.get_cart_items
        #Create empty cart for now for non-logged in user
                                items = []
                                order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
                                cartItems = order['get_cart_items']'''
    

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action :', action)
    print('productId :',productId)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

#csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    print(transaction_id)
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer, complete=False)
    else :
        customer, order = guestOrder(request, data) #create customer and order


    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if float(total) == float(order.get_cart_total):        # this help to prevent manupulation by the user in front end
        order.complete = True
        print('total matched')
        order.status = 'Pending'
    order.date_order = datetime.datetime.now()
    order.save()

    if order.shipping == True :
        ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )

    return JsonResponse('payment complete!', safe=False)

@unauthenticated_user
def userLogin(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('store')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'store/user_login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def registerPage(request):
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')
            

        context = {'form':form}
        return render(request, 'store/register.html', context)


@allowed_user(allowed_roles=['customer'])
def ordersHistory(request):

    data = cartData(request)
    cartItems = data['cartItems']

    customer = request.user.customer
    order = Order.objects.filter(customer=customer, complete=True)
    
    myFilter = OrderFilter(request.GET, queryset=order)
    order = myFilter.qs

    item = []
    for i in order:
        items = i.orderitem_set.all()
        item.append(items)
    item.reverse()
    context = {'item': item,'myFilter':myFilter,'cartItems':cartItems}
    return render(request,'store/orders.html',context)