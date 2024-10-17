from django.contrib.auth.models import User, Group
from django import forms
from django.forms import ModelForm
from decimal import Decimal
from .models import Dishes, Tables, TableCarts, TableCartItems, Orders, OrderItems, Courses
from django.contrib.auth.forms import UserCreationForm

class DishesForm(ModelForm):
    class Meta:
        model = Dishes
        fields = [
            'name',
            'description',
            'image',
            'price',
            'course'
        ]

    name = forms.CharField(required=True) 
    description = forms.CharField(
        required=False,
        widget=forms.widgets.Textarea(attrs={'rows': 4})
    ) 
    image = forms.ImageField(required=False) 
    price = forms.DecimalField(required=True) 
    course = forms.ModelMultipleChoiceField(
        queryset=Courses.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple(),
    )
    
    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')

        # ตรวจสอบว่าค่าราคาเป็น None หรือไม่
        if price is not None and price < 0:
            self.add_error('price', 'ราคาต้องมากกว่า 0')
        
        return cleaned_data

class DishesFilterForm(forms.ModelForm):
    class Meta:
        model = Dishes
        fields = [
            'name',
            'course',
            'price'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'ค้นหาเมนูอาหาร'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'placeholder': 'กรอกราคา'}),
        }

    # ฟิลด์เพิ่มเติมสำหรับช่วงราคาขั้นต่ำและขั้นสูง
    price_min = forms.DecimalField(required=False, label='ราคาขั้นต่ำ', min_value=0)
    price_max = forms.DecimalField(required=False, label='ราคาสูงสุด', min_value=0)

    def clean(self):
        cleaned_data = super().clean()
        price_min = cleaned_data.get('price_min')
        price_max = cleaned_data.get('price_max')

        if price_min and price_max and price_min > price_max:
            self.add_error('price_max', 'ราคาสูงสุดต้องมากกว่าราคาขั้นต่ำ')

        return cleaned_data

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('อีเมลนี้ถูกใช้งานแล้ว')
        return email

class UserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='ชื่อจริง')
    last_name = forms.CharField(max_length=30, required=True, label='นามสกุล')
    email = forms.EmailField(required=True, label='อีเมล')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('อีเมลนี้ถูกใช้งานแล้ว')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("รหัสผ่านทั้งสองต้องตรงกัน")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
            # เพิ่มผู้ใช้เข้าไปในกลุ่ม Staff
            staff_group = Group.objects.get(name='Staff')  # สร้างกลุ่มถ้ายังไม่มี
            user.groups.add(staff_group)  # เพิ่มผู้ใช้เข้าไปในกลุ่ม
        return user