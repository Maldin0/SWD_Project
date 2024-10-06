from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tables, Dishes, TableCarts, TableCartItems, Orders, OrderItems, Courses
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from .forms import DishesForm

# Create your views here.
class MenuListView(View):
    def get(self, request, table_number):
        # ดึงข้อมูลหมวดหมู่และเมนูทั้งหมด
        courses = Courses.objects.all()
        dishes = Dishes.objects.all()

        return render(request, 'menu-list.html', {
            'courses': courses, 
            'dishes': dishes,
            'table_number': table_number  # ส่งหมายเลขโต๊ะไปยังเทมเพลต
        })

class OrderHistoryView(View):
    def get(self, request, table_number):
        # ดึงคำสั่งซื้อทั้งหมดที่สั่งโดยโต๊ะนี้
        orders = Orders.objects.filter(table__number=table_number).order_by('-order_date')
        
        # ตรวจสอบว่ามีคำสั่งซื้อสำหรับโต๊ะนี้หรือไม่
        if not orders.exists():
            no_history = "ไม่มีประวัติการสั่งอาหารสำหรับโต๊ะนี้"
        else:
            no_history = None

        return render(request, 'history.html', {
            'orders': orders,
            'table_number': table_number,
            'no_history': no_history,
        })

class AddToCartView(View):
    def post(self, request, table_number):
        # รับข้อมูลจากฟอร์ม
        dish_id = request.POST.get('dish_id')
        amount = request.POST.get('amount')
        
        # ดึงข้อมูลเมนู
        dish = Dishes.objects.get(pk=dish_id)
        
        # ดึงข้อมูลโต๊ะ
        table = Tables.objects.get(number=table_number)
        
        # ตรวจสอบว่าโต๊ะนี้มีการสั่งอาหารหรือยัง
        table_cart, created = TableCarts.objects.get_or_create(table=table, create_date=None)
        
        # สร้างรายการสั่งอาหาร
        table_cart_item, created = TableCartItems.objects.get_or_create(tableOrder=table_cart, dish=dish)
        table_cart_item.amount = amount
        table_cart_item.save()
        
        return redirect('menu_list', table_number=table_number)

class FromAddMenuView(View):
    def get(self, request):
        form = DishesForm()
        return render(request, 'menu-form.html', {'form': form})
    
    def post(self, request):
        form = DishesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
        return render(request, 'menu-form.html', {'form': form})