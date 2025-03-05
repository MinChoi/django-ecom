from django.contrib import messages
from django.shortcuts import render, redirect
from cart.cart import Cart
from .form import ShippingForm, PaymentForm
from .models import ShippingAddress



def billing_info(request):

    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quantities()
        total = cart.cart_total()

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
