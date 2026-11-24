from .cart import CartManager

def cart_processor(request):
    cart = CartManager(request)
    return {
        'cart': cart,
        'cart_count': len(cart),
        'cart_subtotal': cart.get_total_price(),
        'cart_grand_total': cart.get_grand_total(),
    }
