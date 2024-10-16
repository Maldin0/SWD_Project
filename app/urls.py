from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('staff/menu/', views.StaffMenuListView.as_view(), name='staff_menu_list'),
    path('staff/menu/add/', views.AddDishView.as_view(), name='add_dish'),
    path('staff/menu/edit/<int:dish_id>/', views.EditDishView.as_view(), name='edit_dish'),
    path('staff/menu/delete/<int:dish_id>/', views.DeleteDishView.as_view(), name='delete_dish'),
    path('staff/profile/', views.ProfileView.as_view(), name='profile'),
    path('staff/profile/edit/', views.UserProfileUpdateView.as_view(), name='edit_profile'),
    path('table/<int:table_number>/', views.MenuListView.as_view(), name='menu_list'),
    path('table/<int:table_number>/history/', views.OrderHistoryView.as_view(), name='order_history'),
    path('table/<int:table_number>/cart/', views.CartView.as_view(), name='view_cart'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/add/', views.UserCreateView.as_view(), name='add_user'),
    path('users/delete/<int:user_id>/', views.UserDeleteView.as_view(), name='delete_user'),
    
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)