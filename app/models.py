from django.db import models
# Create your models here.

class Tables(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'AVAILABLE'
        OCCUPIED = 'OCCUPIED'

    number = models.IntegerField()
    status = models.CharField(choices=Status.choices, default=Status.AVAILABLE)


class Courses(models.Model):
    name = models.CharField(max_length=150)


class Dishes(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    course = models.ManyToManyField(Courses)


class TableCarts(models.Model):
    table = models.ForeignKey(Tables, on_delete=models.CASCADE)
    create_date = models.DateTimeField()


class TableCartItems(models.Model):
    tableOrder = models.ForeignKey(TableCarts, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)


class Orders(models.Model):
    table = models.ForeignKey(Tables, on_delete=models.CASCADE)
    order_date = models.DateField()
    remark = models.TextField(null=True, blank=True)


class OrderItems(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING'
        COOKING = 'COOKING'
        SERVING = 'SERVING'
        FINISHED = 'FINISHED'
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)
    status = models.CharField(choices=Status.choices, default=Status.NOT_FINISH)

