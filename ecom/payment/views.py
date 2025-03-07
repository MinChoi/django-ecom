from statistics import quantiles
from django.contrib import messages
from django.shortcuts import render, redirect
from cart.cart import Cart
from django.contrib.auth.models import User
from .form import ShippingForm, PaymentForm
from .models import ShippingAddress, Order, OrderItem
from store.models import Product
import datetime

def process_order(request):
    if request.POST:

        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quantities()
        total = cart.cart_total()

        payment_form = PaymentForm(request.POST or None)

        my_shipping = request.session.get('my_shipping')

        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = total

        if request.user.is_authenticated:
            user = request.user

            new_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            new_order.save()

            # save orderId
            order_id = new_order.pk

            for product in cart_products:
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

            for key, value in quantities.items():
                if int(key) == product.id:
                    create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                    create_order_item.save()

        else:
            new_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            new_order.save()
            # save orderId
            order_id = new_order.pk

            for product in cart_products:
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

            for key, value in quantities.items():
                if int(key) == product.id:
                    create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                    create_order_item.save()

        for key in list(request.session.keys()):
            if key == 'session_key':
                del request.session[key]

        messages.success(request, "Order Placed!")
        return redirect('home')

    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def billing_info(request):

    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quantities()
        total = cart.cart_total()

        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # check if user is logged in
        if request.user.is_authenticated:
            billing_form = PaymentForm
            return render(request, 'payment/billing_info.html', {'cart_products': cart_products, 'quantities': quantities,
                                                             'total': total, 'shipping_info': request.POST, 'billing_form':billing_form})
        else:
            billing_form = PaymentForm
            return render(request, 'payment/billing_info.html', {'cart_products': cart_products, 'quantities': quantities,
                                                             'total': total, 'shipping_info': request.POST, 'billing_form':billing_form})

        shipping_info = request.POST
        return render(request, 'payment/billing_info.html', {'cart_products':cart_products, 'quantities':quantities,
                                                      'total': total, 'shipping_info': request.POST})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quantities()
    total = cart.cart_total()

    if request.user.is_authenticated:
        # this value may return null
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {'cart_products':cart_products, 'quantities':quantities,
                                                         'total':total, 'shipping_form':shipping_form})
    else:
        # guess
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {'cart_products':cart_products, 'quantities':quantities,
                                                         'total':total, 'shipping_form':shipping_form})

def payment_success(request):
    return render(request, 'payment/payment_success.html', {})


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:

        if request.POST:
            _order_id = request.POST['order_id']
            now = datetime.datetime.now()
            _order = Order.objects.filter(id=_order_id)
            _order.update(shipped=False, date_shipped=now)
            messages.success(request, "Shipping Status updated")

        orders = Order.objects.filter(shipped=True)
        return render(request, 'payment/shipped_dash.html', {'orders':orders})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:

        if request.POST:
            _order_id = request.POST['order_id']
            now = datetime.datetime.now()
            _order = Order.objects.filter(id=_order_id)
            _order.update(shipped=True, date_shipped=now)
            messages.success(request, "Shipping Status updated")

        orders = Order.objects.filter(shipped=False)
        return render(request, 'payment/not_shipped_dash.html', {'orders':orders})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        order_items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            _order = Order.objects.filter(id=pk)

            if status == 'true':
                now = datetime.datetime.now()
                _order.update(shipped=True, date_shipped=now)
            else:
                _order.update(shipped=False)
            order = Order.objects.get(id=pk)
            messages.success(request, "Shipping Status updated")

        return render(request, 'payment/orders.html', {'order':order, 'items': order_items})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')

    # if request.user.is_authenticated and request.user.is_superuser:
    #     orders = Order.objects.filter(shipped=False)
    #     return render(request, 'payment/not_shipped_dash.html', {'orders':orders})
    # else:
    #     messages.success(request, "Access Denied")
    #     return redirect('home')

