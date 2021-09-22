from django.db import transaction
from django.shortcuts import render,get_object_or_404
from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Service, Order, Customer, Product  #CartProduct
#from .mixins import CartMixin
from .forms import OrderForm, LoginForm, RegistrationForm
from .utils import recalc_cart
from importlib import import_module
from cart.forms import CartAddProductForm

from django.conf import settings
from django.http import JsonResponse
from django.views.generic import View


class BaseView(View):  #CartMixin
    """"""
    def get(self, request, *args, **kwargs):
        services = Service.objects.all()
        products = Product.objects.all()
        context = {
            'services': services,
            'products': products,
            #'cart': self.cart
        }
        return render(request, 'mainapp/base.html', context)


#class ProductDetailView(DetailView):  #CartMixin
#    """"""
#    context_object_name = 'product'
#    template_name = 'product_detail.html'
#    slug_url_kwarg = 'slug'
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['cart'] = self.cart
#        return context


class ServiceDetailView(DetailView):  #CartMixin
    """"""
    model = Service
    queryset = Service.objects.all()
    context_object_name = 'service'
    template_name = 'service_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class AddToCartView(View):  #CartMixin
    """"""
    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        #cart_product, created = CartProduct.objects.get_or_create(
        #    user=self.cart.owner, cart=self.cart, product=product
        #)
        #if created:
        #    self.cart.products.add(cart_product)
        #recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно добавлен")
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(View):
    """"""
    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        #cart_product = CartProduct.objects.get(
        #    user=self.cart.owner, cart=self.cart, product=product,
        #)
        #self.cart.products.remove(cart_product)
        #cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно удален")
        return HttpResponseRedirect('/cart/')


class ChangeQTYView(View):
    """"""
    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        #cart_product = CartProduct.objects.get(
        #    user=self.cart.owner, cart=self.cart, product=product
        #)
        qty = int(request.POST.get('qty'))
        #cart_product.qty = qty
        #cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Кол-во товара успешно изменено")
        return HttpResponseRedirect('/cart/')


#class CartView(CartMixin, View):
#    """"""
#    def get(self, request, *args, **kwargs):
#        services = Service.objects.all()
#        context = {
#            'cart': self.cart,
#            'services': services
#        }
#        return render(request, 'cart.html', context)


class CheckoutView(View):
    """"""
    def get(self, request, *args, **kwargs):
        services = Service.objects.all()
        form = OrderForm(request.POST or None)
        context = {
            #'cart': self.cart,
            'services': services,
            'form': form
        }
        return render(request, 'checkout.html', context)


class MakeOrderView(View):
    """"""
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеждер с Вами свяжется')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


class ProfileView(View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer).order_by('-created_at')
        services = Service.objects.all()
        return render(
            request,
            'profile.html',
            {'orders': orders, 'cart': self.cart, 'services': services}
        )


def product_detail(request, slug):
    product = get_object_or_404(Product,
                                #id=id,
                                slug=slug,
                                #available=True
                                )
    cart_product_form = CartAddProductForm()
    return render(request, 'mainapp/product_detail.html', {'product': product, 'cart_product_form': cart_product_form})
