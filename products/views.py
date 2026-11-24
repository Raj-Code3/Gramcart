from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Avg, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal

from .models import Product, Category, Brand, Review, Wishlist, ProductImage


def product_list_view(request):
    products = Product.objects.filter(is_available=True).select_related('category', 'brand').prefetch_related('images', 'reviews')
    
    # Query parameters
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    brand_slug = request.GET.get('brand', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    rating_filter = request.GET.get('rating', '').strip()
    in_stock = request.GET.get('in_stock', '').strip()
    sort = request.GET.get('sort', 'featured').strip()

    selected_category = None
    if category_slug:
        selected_category = Category.objects.filter(slug=category_slug).first()
        if selected_category:
            # Include child categories as well
            child_ids = selected_category.subcategories.values_list('id', flat=True)
            all_cat_ids = [selected_category.id] + list(child_ids)
            products = products.filter(category_id__in=all_cat_ids)

    if brand_slug:
        products = products.filter(brand__slug=brand_slug)

    # Search keyword
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(short_description__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()

    # Price range
    try:
        if min_price:
            products = products.filter(price__gte=Decimal(min_price))
        if max_price:
            products = products.filter(price__lte=Decimal(max_price))
    except Exception:
        pass

    # Availability filter
    if in_stock == '1':
        products = products.filter(stock__gt=0)

    # Annotate with average rating for rating filter & sorting
    products = products.annotate(avg_rating=Avg('reviews__rating'))

    if rating_filter and rating_filter.isdigit():
        min_stars = int(rating_filter)
        products = products.filter(avg_rating__gte=min_stars)

    # Sorting
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'rating_desc':
        products = products.order_by('-avg_rating', '-created_at')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    elif sort == 'best_sellers':
        products = products.order_by('-is_best_seller', '-created_at')
    else: # featured
        products = products.order_by('-is_featured', '-is_best_seller', '-created_at')

    # Aggregated stats for filter sidebars
    all_categories = Category.objects.filter(parent=None).prefetch_related('subcategories')
    all_brands = Brand.objects.annotate(product_count=Count('products')).filter(product_count__gt=0)
    
    # Deals of the day & Featured section for top carousel
    deals = Product.objects.filter(is_deal_of_the_day=True, is_available=True)[:4]
    featured_categories = Category.objects.filter(is_featured=True)[:6]

    total_results_count = products.count()

    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page', 1)
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

    user_wishlist_ids = set()
    if request.user.is_authenticated:
        user_wishlist_ids = set(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    context = {
        'products': products_page,
        'query': query,
        'selected_category': selected_category,
        'category_slug': category_slug,
        'brand_slug': brand_slug,
        'min_price': min_price,
        'max_price': max_price,
        'rating_filter': rating_filter,
        'in_stock': in_stock,
        'sort': sort,
        'all_categories': all_categories,
        'all_brands': all_brands,
        'deals': deals,
        'featured_categories': featured_categories,
        'total_results_count': total_results_count,
        'user_wishlist_ids': user_wishlist_ids,
    }
    return render(request, 'products/product_list.html', context)


def category_products_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    # Redirect to standard list with category parameter
    return redirect(f"/?category={slug}")


def product_detail_view(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category', 'brand').prefetch_related('images', 'reviews__user'),
        slug=slug
    )
    
    # Related products in same category
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]

    # User's existing review if any
    user_review = None
    is_in_wishlist = False
    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()
        is_in_wishlist = Wishlist.objects.filter(product=product, user=request.user).exists()

    rating_dist = product.get_rating_distribution()

    context = {
        'product': product,
        'images': product.images.all(),
        'reviews': product.reviews.all(),
        'related_products': related_products,
        'user_review': user_review,
        'is_in_wishlist': is_in_wishlist,
        'rating_dist': rating_dist,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def add_review_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        headline = request.POST.get('headline', '').strip()
        comment = request.POST.get('comment', '').strip()

        if not rating or not (1 <= int(rating) <= 5):
            messages.error(request, "Please select a valid star rating (1-5).")
            return redirect('products:product_detail', slug=slug)

        if not headline or not comment:
            messages.error(request, "Please fill in both a headline and your review thoughts.")
            return redirect('products:product_detail', slug=slug)

        review, created = Review.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={
                'rating': int(rating),
                'headline': headline,
                'comment': comment,
                'is_verified_purchase': True  # Simulated verified purchase
            }
        )

        messages.success(request, "Thank you! Your customer review has been published.")
    return redirect('products:product_detail', slug=slug)


@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'products/wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def toggle_wishlist_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
    
    if wishlist_item:
        wishlist_item.delete()
        is_added = False
        message = f"Removed '{product.name}' from your Wishlist."
    else:
        Wishlist.objects.create(user=request.user, product=product)
        is_added = True
        message = f"Added '{product.name}' to your Wishlist!"

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'is_added': is_added,
            'message': message,
            'wishlist_count': Wishlist.objects.filter(user=request.user).count()
        })

    messages.info(request, message)
    return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))


def quick_search_api(request):
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'results': []})

    products = Product.objects.filter(
        Q(name__icontains=query) | Q(category__name__icontains=query) | Q(brand__name__icontains=query),
        is_available=True
    )[:6]

    results = []
    for p in products:
        results.append({
            'id': p.id,
            'name': p.name,
            'price': str(p.current_price),
            'url': p.get_absolute_url(),
            'image': p.primary_image_url,
            'category': p.category.name,
            'rating': p.average_rating
        })

    return JsonResponse({'results': results})



# ---------- Policy pages (footer) ----------
from .policies import POLICIES, grouped as policy_groups


def policy_view(request, slug):
    from django.http import Http404
    item = POLICIES.get(slug)
    if not item:
        raise Http404('Policy not found')
    group, title, body, link = item
    return render(request, 'products/policy.html', {
        'title': title, 'group': group, 'paragraphs': body.split('\n'),
        'official_link': link, 'siblings': [(s, t) for s, t in policy_groups()[group] if s != slug],
    })


def policy_index_view(request):
    return render(request, 'products/policy_index.html', {'groups': policy_groups()})
