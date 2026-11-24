from .models import Category, Wishlist

def categories_processor(request):
    categories = Category.objects.filter(parent=None).prefetch_related('subcategories')
    wishlist_count = 0
    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    
    return {
        'all_departments': categories,
        'wishlist_count': wishlist_count,
    }


def policy_links_processor(request):
    from .policies import grouped, STARTUP, ECOM
    g = grouped()
    return {'policy_groups': {'startup': g[STARTUP], 'ecom': g[ECOM]}}
