from django.urls import path
from . import views

urlpatterns = [
    path('staff/', views.MenuListView.as_view(), name='staff_menu_list'),
    path('table/<int:table_number>/', views.MenuListView.as_view(), name='menu_list'),
    path('table/<int:table_number>/history/', views.OrderHistoryView.as_view(), name='order_history'),
    path('table/<int:table_number>/cart/', views.ViewCartView.as_view(), name='view_cart'),
]