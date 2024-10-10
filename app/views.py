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
from django.db import IntegrityError
from .forms import DishesForm
from datetime import date, datetime

# Create your views here.
class MenuListView(View):
    def get(self, request, table_number):
        # ดึงข้อมูลหมวดหมู่และเมนูทั้งหมด
        courses = Courses.objects.all()
        dishes = Dishes.objects.all()
        table_number = Tables.objects.get(pk=table_number)

        return render(request, 'menu-list.html', {
            'courses': courses, 
            'dishes': dishes,
            'table_number': table_number  # ส่งเลขโต๊ะไป template
        })

    def post(self, request, table_number):
        # รับข้อมูลจากฟอร์ม
        dish_id = request.POST.get('dish_id')
        amount = request.POST.get('amount')
        
        # ดึงข้อมูลเมนู
        dish = Dishes.objects.get(pk=dish_id)
        
        # ดึงข้อมูลโต๊ะ
        table = Tables.objects.get(number=table_number)
        
        # ตรวจสอบว่ามีการสร้างตะกร้าหรือยัง ถ้าไม่มีให้สร้างใหม่
        table_cart, created = TableCarts.objects.get_or_create(
            table=table, defaults={'create_date': datetime.now()}
        )

        # ตรวจสอบการสร้างรายการสั่งอาหาร
        try:
            table_cart_item, created = TableCartItems.objects.get_or_create(
                table_order=table_cart, dish=dish
            )

            # ถ้ามีรายการอาหารอยู่แล้วให้อัปเดตจำนวน
            if not created:
                table_cart_item.amount += int(amount)
            else:
                table_cart_item.amount = int(amount)

            table_cart_item.save()

        except IntegrityError as e:
            # แสดง error message เพื่อ debug ปัญหา
            return JsonResponse({"error": f"เกิดข้อผิดพลาด: {str(e)}"}, status=400)

        return redirect('menu_list', table_number=table_number)

    

class StaffMenuListView(View):
    def get(self, request):
        # ดึงข้อมูลหมวดหมู่และเมนูทั้งหมด
        courses = Courses.objects.all()
        dishes = Dishes.objects.all()

        return render(request, 'staff_menu-list.html', {
            'courses': courses, 
            'dishes': dishes,
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
            'total_amount': total_amount,  # ส่งยอดรวมไปยัง template
            'table_number': table_number   # ส่ง table_number ไปยัง template ด้วย
        })
