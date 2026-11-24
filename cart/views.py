from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal

from products.models import Product
from .cart import CartManager
from .models import Cart, CartItem


def cart_detail_view(request):
    cart = CartManager(request)
    
    # Check free shipping progress (e.g. Free shipping at ₹999)
    free_shipping_threshold = Decimal('999.00')
    subtotal = cart.get_total_price()
    amount_needed_for_free_shipping = max(Decimal('0.00'), free_shipping_threshold - subtotal)
    free_shipping_progress = min(100, int((subtotal / free_shipping_threshold) * 100)) if free_shipping_threshold > 0 else 100

    saved_items = []
    if request.user.is_authenticated:
        db_cart, _ = Cart.objects.get_or_create(user=request.user)
        saved_items = db_cart.items.filter(is_saved_for_later=True).select_related('product')

    context = {
        'cart': cart,
        'free_shipping_threshold': free_shipping_threshold,
        'amount_needed_for_free_shipping': amount_needed_for_free_shipping,
        'free_shipping_progress': free_shipping_progress,
        'saved_items': saved_items,
    }
    return render(request, 'cart/cart_detail.html', context)


@require_POST
def cart_add_view(request, product_id):
    cart = CartManager(request)
    product = get_object_or_404(Product, id=product_id)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1

    if quantity < 1:
        quantity = 1

    if not product.in_stock:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Product is currently out of stock.'}, status=400)
        messages.error(request, f"Sorry, '{product.name}' is currently out of stock.")
        return redirect(product.get_absolute_url())

    cart.add(product=product, quantity=quantity)

    # If user wants to "Buy Now", redirect directly to checkout
    if request.POST.get('action') == 'buy_now':
        return redirect('orders:checkout')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': f"Added '{product.name}' to your cart!",
            'cart_count': len(cart),
            'cart_subtotal': str(cart.get_total_price()),
        })

    messages.success(request, f"Added {quantity}x '{product.name}' to your cart.")
    return redirect('cart:cart_detail')


@require_POST
def cart_update_view(request, product_id):
    cart = CartManager(request)
    product = get_object_or_404(Product, id=product_id)
    
    action = request.POST.get('action')
    try:
        if action == 'increase':
            cart.add(product=product, quantity=1, override_quantity=False)
        elif action == 'decrease':
            # Decrement by 1
            current_qty = cart.cart.get(str(product.id), {}).get('quantity', 0)
            if current_qty > 1:
                cart.cart[str(product.id)]['quantity'] = current_qty - 1
                cart.save()
            else:
                cart.remove(product)
        elif 'quantity' in request.POST:
            qty = int(request.POST.get('quantity'))
            if qty > 0:
                cart.add(product=product, quantity=qty, override_quantity=True)
            else:
                cart.remove(product)
    except Exception as e:
        messages.error(request, f"Error updating cart: {e}")

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'cart_count': len(cart),
            'cart_subtotal': str(cart.get_total_price()),
            'cart_tax': str(cart.get_tax()),
            'cart_shipping': str(cart.get_shipping()),
            'cart_grand_total': str(cart.get_grand_total()),
        })

    return redirect('cart:cart_detail')


def cart_remove_view(request, product_id):
    cart = CartManager(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f"Removed '{product.name}' from your shopping cart.")
    return redirect('cart:cart_detail')


@require_POST
def save_for_later_view(request, product_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Please log in to save items for later.")
        return redirect('accounts:login')

    cart = CartManager(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Remove from active cart
    cart.remove(product)

    # Add to DB saved list
    db_cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=db_cart, product=product)
    cart_item.is_saved_for_later = True
    cart_item.save()

    messages.info(request, f"'{product.name}' saved for later.")
    return redirect('cart:cart_detail')


@require_POST
def move_to_cart_view(request, product_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    db_cart, _ = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.filter(cart=db_cart, product=product).first()
    
    if cart_item:
        cart_item.delete()

    cart = CartManager(request)
    cart.add(product=product, quantity=1)
    
    messages.success(request, f"Moved '{product.name}' back to cart.")
    return redirect('cart:cart_detail')

