from django.shortcuts import render, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from products.models import Products, Category
from order.models import ShopCart, ShopCartForm
from user.models import UserProfile
from order.models import Order, OrderForm, OrderProduct
from django.utils.crypto import get_random_string

# Create your views here.


def index(request):
    return HttpResponse('order page')


@login_required(login_url='/login')  # Check login
def addtoshopcart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    checkproduct = ShopCart.objects.filter(products_id=id)

    if checkproduct:
        control = 1  # The product is in the cart
    else:
        control = 0  # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update  shopcart
                data = ShopCart.objects.get(products_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else:  # Inser to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.products_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to Shopcart ")
        return HttpResponseRedirect(url)
    else:  # if there is no post
        if control == 1:  # Update  shopcart
            data = ShopCart.objects.get(products_id=id)
            data.quantity += 1
            data.save()  #
        else:  # Inser to Shopcart
            data = ShopCart()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.products_id = id
            data.quantity = 1
            data.save()  #
        messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect(url)


def shopcart(request):
    current_user = request.user
    category = Category.objects.all()
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.amount
    context = {
        'category': category,
        'shopcart': shopcart,
        'total': total,
    }
    return render(request, 'cart.html', context)


@login_required(login_url='/login')  # Check login
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, 'your item is deleted form cart!')
    return HttpResponseRedirect('/order/shopcart')


def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    profile = UserProfile.objects.get(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.products.price * rs.quantity
    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        # return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............

            data = Order()
            # get product quantity from form
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.country = form.cleaned_data['country']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()  # random cod
            data.code = ordercode
            data.save()

            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id  # Order Id
                detail.product_id = rs.products_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.amount = rs.amount
                detail.price = rs.products.price
                detail.save()
                product=Products.objects.get(id=rs.products_id)
                product.amount-=rs.products.price
                product.save()
                # ***Reduce quantity of sold product from Amount of Product
               
                # ************ <> *****************

            # Clear & Delete shopcart
            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0
            messages.success(
                request, "Your Order has been completed. Thank you ")
            return render(request, 'Order_Completed.html', {'ordercode': ordercode, 'category': category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               'form': form,
               'profile': profile,
               }
    return render(request,'order_form.html', context)
