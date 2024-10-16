from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from decimal import Decimal
from .models import Dishes, Tables, TableCarts, TableCartItems, Orders, OrderItems, Courses

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
        widget=forms.CheckboxSelectMultiple(),  # ใช้ CheckboxSelectMultiple สำหรับแสดง checkbox
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
        
    # Add custom validation if needed
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email