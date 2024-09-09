from django.db import models

from users.models import Profile


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(Profile, related_name='suppliers', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    supplier = models.ForeignKey(Supplier, related_name='supplier', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=256)
    category = models.ForeignKey(Category, related_name='sub_categories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    PRODUCT_STATUS = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ]
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=PRODUCT_STATUS, default='available')
    sub_category = models.ForeignKey(SubCategory, related_name='sub_categories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Order(models.Model):
    ORDER_STATUS = [
        ('confirmed', 'Confirmed'),
        ('dispatched', 'Dispatched'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_orders')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} by {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.price = self.product.price
        self.total_price = self.quantity * self.price
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for Order #{self.order.id}"
