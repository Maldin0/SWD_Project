from django.db import models

# Create your models here.

class Tables(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'AVAILABLE'
        OCCUPIED = 'OCCUPIED'

    number = models.IntegerField()
    status = models.CharField(choices=Status.choices, default=Status.AVAILABLE)

    def __str__(self):
        return str(self.number)


class Courses(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Dishes(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='dishes/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    course = models.ManyToManyField(Courses)

    def __str__(self):
        return self.name


class TableCarts(models.Model):
    table = models.ForeignKey(Tables, on_delete=models.CASCADE)
    create_date = models.DateTimeField()


class TableCartItems(models.Model):
    table_order  = models.ForeignKey(TableCarts, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)


class Orders(models.Model):
    table = models.ForeignKey(Tables, on_delete=models.CASCADE)
    order_date = models.DateField()
    remark = models.TextField(null=True, blank=True)


class OrderItems(models.Model):
    class Status(models.TextChoices):
        NOT_FINISH = 'NOT_FINISH'
        PENDING = 'PENDING'
        COOKING = 'COOKING'
        SERVING = 'SERVING'
        FINISHED = 'FINISHED'
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)
    status = models.CharField(choices=Status.choices, default=Status.NOT_FINISH)

