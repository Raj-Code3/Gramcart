from django.contrib import admin
from .models import Category, Brand, Product, ProductImage, Review, Wishlist


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2
    fields = ('image', 'image_url', 'alt_text', 'is_primary', 'order')


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('user', 'rating', 'headline', 'comment', 'is_verified_purchase', 'created_at')
    can_delete = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'is_featured', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_featured', 'parent')
    search_fields = ('name', 'description')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'website')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'brand', 'price', 'discount_price', 'stock', 'is_available', 'is_best_seller', 'is_featured')
    list_filter = ('is_available', 'is_featured', 'is_best_seller', 'is_deal_of_the_day', 'category', 'brand')
    list_editable = ('price', 'discount_price', 'stock', 'is_available', 'is_best_seller', 'is_featured')
    search_fields = ('name', 'sku', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ReviewInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'headline', 'is_verified_purchase', 'created_at')
    list_filter = ('rating', 'is_verified_purchase', 'created_at')
    search_fields = ('headline', 'comment', 'user__username', 'product__name')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    search_fields = ('user__username', 'product__name')

