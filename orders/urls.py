from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('success/<str:order_number>/', views.order_success_view, name='order_success'),
    path('detail/<str:order_number>/', views.order_detail_view, name='order_detail'),
    path('history/', views.order_history_view, name='order_history'),
    path('cancel/<str:order_number>/', views.cancel_order_view, name='order_cancel'),
    path('tracking/', views.track_order_view, name='order_tracking'),
]
