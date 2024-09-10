from django.db import models

# Create your models here.

class Table(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'AVAILABLE'
        OCCUPIED = 'OCCUPIED'

    number = models.IntegerField()
    status = models.CharField(choices=Status.choices, default=Status.AVAILABLE)

class DishCategory(models.Model):
    name = models.CharField(max_length=150)

class Dish(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(DishCategory)

class TableCart(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    create_date = models.DateTimeField()

class TableCartItem(models.Model):
    tableOrder = models.ForeignKey(TableCart, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)

class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    order_date = models.DateField()
    remark = models.TextField(null=True, blank=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)
