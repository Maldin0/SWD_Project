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
from django.db.models import Q
from .forms import DishesForm, DishesFilterForm
from datetime import date, datetime

# Create your views here.
class MenuListView(View):
    def get(self, request, table_number=None):
        # ดึงข้อมูลหมวดหมู่ทั้งหมด
        courses = Courses.objects.all()
        dishes = Dishes.objects.all()

        # ค่าที่ค้นหาหรือกรองจาก request
        search_query = request.GET.get('search', '')
        course_filter = request.GET.get('course_filter', '')

        # Filter by search query (ถ้ามีการค้นหา)
        if search_query:
            dishes = dishes.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

        # Filter by course (ถ้าเลือกหมวดหมู่)
        if course_filter:
            dishes = dishes.filter(course__id=course_filter)

        # ถ้ามี table_number จะให้แสดงเมนูสำหรับโต๊ะนั้น
        table = None
        if table_number is not None:
            table = Tables.objects.get(number=table_number)

        return render(request, 'menu-list.html', {
            'courses': courses, 
            'dishes': dishes,
            'table_number': table,
            'search_query': search_query,  # ส่ง search query ไป template
            'course_filter': course_filter,  # ส่ง course filter ไป template
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


class AddDishView(View):
    def get(self, request):
        form = DishesForm()
        return render(request, 'menu-form.html', {'form': form})
        
    def post(self, request):
        form = DishesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('staff_menu_list')
        return render(request, 'menu-form.html', {'form': form})

class EditDishView(View):
    def get(self, request, dish_id):
        # ดึงข้อมูลเมนูจากฐานข้อมูล
        dish = Dishes.objects.get(pk=dish_id)
        form = DishesForm(instance=dish)

        return render(request, 'menu-form.html', {'form': form})

    def post(self, request, dish_id):
        # ดึงข้อมูลเมนูที่ต้องการแก้ไข
        dish = Dishes.objects.get(pk=dish_id)
        # กรอกข้อมูลใหม่ลงฟอร์มแล้วตรวจสอบความถูกต้อง
        form = DishesForm(request.POST, request.FILES, instance=dish)
        if form.is_valid():
            form.save()  # บันทึกการเปลี่ยนแปลง
            return redirect('staff_menu_list')  # กลับไปยังหน้าแสดงรายการเมนูหลังบันทึกสำเร็จ
        return render(request, 'menu-form.html', {'form': form})

class DeleteDishView(View):
    def post(self, request, dish_id):
        # ดึงข้อมูลเมนูที่ต้องการลบ
        dish = Dishes.objects.get(pk=dish_id)
        dish.delete()  # ลบเมนูออกจากฐานข้อมูล
        return redirect('staff_menu_list')  # กลับไปยังหน้าแสดงรายการเมนู


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

            # เพิ่มยอดรวมของแต่ละรายการใน cart_items และคำนวณยอดรวมทั้งหมด
            for item in cart_items:
                # คำนวณยอดรวมของแต่ละรายการ
                item.total_price = item.dish.price * item.amount  
                
                # เพิ่มยอดรวมทั้งหมด
                total_amount += item.total_price

        return render(request, 'cart.html', {
            'table': table,
            'cart_items': cart_items,
            'total_amount': total_amount,  # ส่งยอดรวมทั้งหมดไปยัง template

        })

    def post(self, request, table_number):
        # ดึงข้อมูลโต๊ะ
        table = Tables.objects.get(number=table_number)

        # สร้างรายการสั่งอาหาร (Order) ใหม่
        table_cart = TableCarts.objects.filter(table=table).first()
        remark = request.POST.get('remark', '')
        order = Orders.objects.create(
            order_date=datetime.now(),
            remark=remark,
            table=table,
        )

        # สร้างรายการ OrderItems จากรายการใน cart
        cart_items = TableCartItems.objects.filter(table_order=table_cart)
        for item in cart_items:
            OrderItems.objects.create(
                amount=item.amount,
                status=OrderItems.Status.PENDING,
                dish=item.dish,
                order=order,
            )

        # ลบตะกร้าอาหารหลังจากยืนยันการสั่งแล้ว
        table_cart.delete()

        # Redirect ไปหน้าอื่นหลังจากยืนยันเสร็จแล้ว
        return redirect('order_history', table_number=table_number)