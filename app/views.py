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
    def get(self, request, table_number=None):  # กำหนดค่า table_number เป็น optional
        # ดึงข้อมูลหมวดหมู่และเมนูทั้งหมด
        courses = Courses.objects.all()
        dishes = Dishes.objects.all()

        # ตรวจสอบว่ามี table_number หรือไม่
        if table_number:
            try:
                table_number = Tables.objects.get(pk=table_number)
            except Tables.DoesNotExist:
                table_number = None
        else:
            table_number = None

        return render(request, 'menu-list.html', {
            'courses': courses, 
            'dishes': dishes,
            'table_number': table_number  # ส่งเลขโต๊ะหรือ None ไป template
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

class ViewCartView(View):
    def get(self, request, table_number):
        # ดึงข้อมูลโต๊ะ
        table = Tables.objects.get(number=table_number)
        
        # ดึงข้อมูลรายการอาหารในตะกร้า
        table_cart = TableCarts.objects.filter(table=table).first()
        cart_items = []
        total_amount = 0

        if table_cart:
            cart_items = TableCartItems.objects.filter(table_order=table_cart)
            # คำนวณยอดรวม
            total_amount = sum(item.dish.price * item.amount for item in cart_items)

            # เพิ่มยอดรวมของแต่ละรายการใน cart_items
            for item in cart_items:
                item.total_price = item.dish.price * item.amount  # เพิ่มยอดรวมของแต่ละรายการ

        return render(request, 'cart.html', {
            'table': table,
            'cart_items': cart_items,
            'total_amount': total_amount  # ส่งยอดรวมไปยัง template
        })

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