from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from decimal import Decimal
import datetime

from .models import Order, OrderItem
from .forms import CheckoutForm
from cart.cart import CartManager
from accounts.models import Address
from products.models import Product


def checkout_view(request):
    cart = CartManager(request)
    
    # Check if cart is empty
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty. Add products before proceeding to checkout.")
        return redirect('products:product_list')

    # Calculate shipping options
    subtotal = cart.get_total_price()
    tax = cart.get_tax()

    user_addresses = []
    default_address = None
    initial_data = {}

    if request.user.is_authenticated:
        user_addresses = Address.objects.filter(user=request.user)
        default_address = user_addresses.filter(is_default_shipping=True).first() or user_addresses.first()
        
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
        }
        if default_address:
            initial_data.update({
                'full_name': default_address.full_name,
                'phone_number': default_address.phone_number,
                'shipping_address': default_address.street_address,
                'apartment_suite': default_address.apartment_suite or '',
                'city': default_address.city,
                'state': default_address.state,
                'postal_code': default_address.postal_code,
                'country': default_address.country,
                'delivery_notes': default_address.delivery_instructions or '',
            })

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Calculate shipping fee based on selection
            delivery_method = form.cleaned_data['delivery_method']
            if delivery_method == 'express':
                shipping_fee = Decimal('149.00')
            elif delivery_method == 'same_day':
                shipping_fee = Decimal('249.00')
            else:
                shipping_fee = cart.get_shipping()

            grand_total = subtotal + tax + shipping_fee

            # Atomic transaction to guarantee order & stock consistency
            with transaction.atomic():
                # Verify stock
                for item in cart:
                    prod = item['product']
                    if prod.stock < item['quantity']:
                        messages.error(request, f"Sorry, '{prod.name}' only has {prod.stock} items remaining in stock.")
                        return redirect('cart:cart_detail')

                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    full_name=form.cleaned_data['full_name'],
                    email=form.cleaned_data['email'],
                    phone_number=form.cleaned_data['phone_number'],
                    shipping_address=form.cleaned_data['shipping_address'],
                    apartment_suite=form.cleaned_data['apartment_suite'],
                    city=form.cleaned_data['city'],
                    state=form.cleaned_data['state'],
                    postal_code=form.cleaned_data['postal_code'],
                    country=form.cleaned_data['country'],
                    delivery_method=delivery_method,
                    payment_method=form.cleaned_data['payment_method'],
                    payment_status='paid', # Mock payment success
                    order_status='ordered',
                    subtotal=subtotal,
                    shipping_fee=shipping_fee,
                    tax_amount=tax,
                    grand_total=grand_total,
                    delivery_notes=form.cleaned_data['delivery_notes'],
                )

                # Create OrderItems and decrease inventory stock
                for item in cart:
                    prod = item['product']
                    OrderItem.objects.create(
                        order=order,
                        product=prod,
                        product_name=prod.name,
                        product_image_url=prod.primary_image_url,
                        price=item['price'],
                        quantity=item['quantity']
                    )
                    # Decrement inventory stock
                    prod.stock -= item['quantity']
                    if prod.stock == 0:
                        prod.is_available = False
                    prod.save()

                # Optionally save new address if checked
                if request.user.is_authenticated and form.cleaned_data.get('save_address'):
                    if not Address.objects.filter(user=request.user, street_address=form.cleaned_data['shipping_address']).exists():
                        Address.objects.create(
                            user=request.user,
                            full_name=form.cleaned_data['full_name'],
                            phone_number=form.cleaned_data['phone_number'],
                            street_address=form.cleaned_data['shipping_address'],
                            apartment_suite=form.cleaned_data['apartment_suite'],
                            city=form.cleaned_data['city'],
                            state=form.cleaned_data['state'],
                            postal_code=form.cleaned_data['postal_code'],
                            country=form.cleaned_data['country'],
                            delivery_instructions=form.cleaned_data['delivery_notes'],
                            is_default_shipping=not user_addresses.exists()
                        )

            # Clear cart session
            cart.clear()
            messages.success(request, f"Your order #{order.order_number} has been placed successfully!")
            return redirect('orders:order_success', order_number=order.order_number)
        else:
            messages.error(request, "Please check your entered details and try again.")
    else:
        form = CheckoutForm(initial=initial_data)

    context = {
        'form': form,
        'cart': cart,
        'user_addresses': user_addresses,
        'default_address': default_address,
        'subtotal': subtotal,
        'tax': tax,
        'standard_shipping': cart.get_shipping(),
        'express_shipping': Decimal('149.00'),
        'same_day_shipping': Decimal('249.00'),
    }
    return render(request, 'orders/checkout.html', context)


def order_success_view(request, order_number):
    order = get_object_or_404(Order.objects.prefetch_related('items__product'), order_number=order_number)
    return render(request, 'orders/order_success.html', {'order': order})


def order_detail_view(request, order_number):
    order = get_object_or_404(Order.objects.prefetch_related('items__product'), order_number=order_number)
    
    # Check permissions (either the user's order or guest lookup)
    if order.user and order.user != request.user and not request.user.is_staff:
        messages.error(request, "You do not have permission to view this order.")
        return redirect('products:product_list')

    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def cancel_order_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    if order.order_status in ['ordered', 'processing']:
        order.order_status = 'cancelled'
        order.save()

        # Restock products
        for item in order.items.all():
            if item.product:
                item.product.stock += item.quantity
                item.product.is_available = True
                item.product.save()

        messages.info(request, f"Order #{order.order_number} has been cancelled and items restocked.")
    else:
        messages.error(request, f"Order cannot be cancelled as it has already been {order.get_order_status_display().lower()}.")

    return redirect('orders:order_detail', order_number=order.order_number)


def track_order_view(request):
    order = None
    query = request.GET.get('order_query', '').strip()
    
    if query:
        order = Order.objects.filter(
            Q(order_number__iexact=query) | Q(tracking_number__iexact=query)
        ).first()
        if not order:
            messages.error(request, f"No order found matching '{query}'. Please check your order ID or tracking number.")

    return render(request, 'orders/order_tracking.html', {'order': order, 'query': query})

