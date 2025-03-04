from django.shortcuts import render
from cart.cart import Cart
from .form import ShippingForm
from .models import ShippingAddress


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quantities()
    total = cart.cart_total()

    if request.user.is_authenticated:
        # this value may return null
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {'cart_products':cart_products, 'quantities':quantities, 'total':total})
    else:
        # guess
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {'cart_products':cart_products, 'quantities':quantities, 'total':total})

def payment_success(request):
    return render(request, 'payment/payment_success.html', {})
