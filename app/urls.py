from django.urls import path
from . import views

urlpatterns = [
    # Landing Page URLs
    path('', views.landing, name='landing'),
    path('landing/menu/', views.menu, name='landing_menu'),
    path('landing/reservation/', views.reservation, name='landing_reservation'),
    path('contact/', views.contact, name='contact'),

    # Admin Authentication
        path('admin-login/', views.admin_login, name='admin_login'),

    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.logout_view, name='logout'),

       # Menu Management
    path('menu/', views.menu_list, name='menu_list'),
    path('menu/add/', views.add_menu_item, name='add_menu_item'),
    path('menu/edit/<int:item_id>/', views.edit_menu_item, name='edit_menu_item'),
    path('menu/delete/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),

    # Orders Management
    path('orders/', views.view_orders, name='view_orders'),
    path('orders/process/<int:order_id>/', views.process_order, name='process_order'),
    path('orders/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),

    # Reservations Management
    path('reservations/', views.view_reservations, name='view_reservations'),
    path('reservations/confirm/<int:res_id>/', views.confirm_reservation, name='confirm_reservation'),
    path('reservations/cancel/<int:res_id>/', views.cancel_reservation, name='cancel_reservation'),
    
    
    
     path('explore-menu/', views.menu_items_view, name='menu_items_view'),
     
     
      path('name/', views.menu_page, name='name'),  # your menu page
   path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('order-summary/', views.order_summary, name='order_summary'),
    path('increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('admin-orders/', views.admin_orders, name='admin_orders'),
]
