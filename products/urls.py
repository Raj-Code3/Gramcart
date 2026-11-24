from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list_view, name='product_list'),
    path('category/<slug:slug>/', views.category_products_view, name='category_products'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('product/<slug:slug>/review/', views.add_review_view, name='add_review'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist_view, name='toggle_wishlist'),
    path('policies/', views.policy_index_view, name='policy_index'),
    path('policies/<slug:slug>/', views.policy_view, name='policy'),
    path('api/quick-search/', views.quick_search_api, name='quick_search_api'),
]
