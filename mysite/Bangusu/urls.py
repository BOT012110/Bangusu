from django.urls import path
from . import views
from .views import add_to_cart, remove_from_cart, remove_single_item_from_cart, add_single_item_to_cart

app_name = 'bnsu'
urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('w_page/', views.WomanPage.as_view(), name='w_page'),
    path('m_page/', views.ManPage.as_view(), name='m_page'),
    path('all_page/', views.AllPage.as_view(), name='all_page'),
    path('filter/', views.FilterCategory.as_view(), name='filter'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    path('product_detail/<slug>', views.ProductDetail.as_view(), name='product_detail'),
    path('add-to-card/<slug>/', add_to_cart, name='add-to-card'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('add-single-item-to-cart/<slug>/', add_single_item_to_cart, name='add-single-item-to-cart')
]
