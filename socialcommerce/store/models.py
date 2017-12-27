from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()

class Store(models.Model):
    owner = models.OneToOneField(User, related_name="store_owned", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=f'stores/%Y/%m/%d', blank=True)
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    store = models.ForeignKey(Store, related_name="store_product", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        index_together = (('id', 'slug'),)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    DELIVERED = "delivered"
    PROCESSING = "processing"
    AWAITING = "awaiting"
    ORDER_STATUS = (
        (CONFIRMED, "Confirmed"),
        (CANCELLED, 'Cancelled'),
        (DELIVERED, 'Delivered'),
        (PROCESSING, 'Processing'),
        (AWAITING, 'Awaiting'),
    )
    product = models.ForeignKey(Product, related_name="order", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="orders_by_user", on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name="orders_to_store", on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=ORDER_STATUS, default=AWAITING)
    processing_time = models.CharField(max_length=255)
    quantity =models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)

    def __str__(self):
        return f'order of {self.product.name} from {self.user.first_name} to {self.store.name}'
