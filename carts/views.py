from django.shortcuts import render, redirect

from orders.models import Order
from products.models import Product
from .models import Cart

def cart_home(request):
	cart_obj = Cart.objects.new_or_get(request)
	return render (request, 'carts/cart_home.html', {"cart":cart_obj})

def cart_update(request):
	print(request.POST)
	product_id = request.POST.get('product_id')
	if product_id is not None:
		try:
			product_obj = Product.objects.get(id=product_id)
		except Product.DoesNotExist:
			return redirect("cart:home")
	
	cart_obj = Cart.objects.new_or_get(request)
	if product_obj in cart_obj.products.all():
		cart_obj.products.remove(product_obj)
	else:
		cart_obj.products.add(product_obj)

	request.session['cart_items'] = cart_obj.products.count()
	return redirect("cart:home")

def checkout_home(request):
	cart_obj = Cart.objects.new_or_get(request)
	order_obj = None
	if cart_obj.products.count() == 0:
		return redirect("cart:home")
	else:
		order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
	return render(request, "carts/checkout.html", {"object": order_obj})