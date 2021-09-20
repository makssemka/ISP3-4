from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from mainapp.models import Product
from django.contrib import messages
from .cart import Cart
from .forms import CartAddProductForm
from django.http import HttpResponseRedirect
from django.http import HttpResponseRedirect


@require_POST
def cart_add(request, slug):
    if request.user.is_authenticated:
        cart = Cart(request)
        print(cart)
        product = get_object_or_404(Product, slug=slug)
        print(product)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                     quantity=cd['quantity'],
                     update_quantity=cd['update'])
    else:
        return HttpResponseRedirect('/login/')
    return redirect('cart:cart_detail')


def cart_remove(request, slug):
    cart = Cart(request)
    product = Product.objects.get(slug=slug)
    cart.remove(product)
    messages.add_message(request, messages.INFO, "Товар успешно удален")
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})
