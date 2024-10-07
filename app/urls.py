from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.StaffMenuListView.as_view(), name='staff_menu_list'),
    path('menu/<int:table_number>/', views.MenuListView.as_view(), name='menu_list'),
    path('history/<int:table_number>/', views.OrderHistoryView.as_view(), name='order_history'),
    path('add-menu/', views.FromAddMenuView.as_view(), name='add_menu'),
]