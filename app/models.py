from django.db import models

# Create your models here.


from django.db import models
from django.utils import timezone

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processed', 'Processed'),
        ('Cancelled', 'Cancelled'),
    ]
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    order_date = models.DateTimeField(default=timezone.now)
    items = models.ManyToManyField(MenuItem)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Reservation by {self.customer_name} on {self.date}"



class OrderItem(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', null=True, blank=True)

    def get_total_price(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.menu_item.name} (x{self.quantity})"
