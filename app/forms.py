from django.forms import ModelForm
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
    
    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        if price < 0:
            self.add_error('price', 'ราคาต้องมากกว่า 0')
        return cleaned_data