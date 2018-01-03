from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
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
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

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

class AvailableProductQuerySet(models.QuerySet):

    def available(self):
        return self.filter(available=True)

    def get_interest_product(self, user_interest):
        return self.filter(category_id__in=user_interest)

    def filter_products(self, **kwargs):
        q = kwargs['query'].get('q')
        ql = kwargs['query'].get('l')
        qc = kwargs['query'].get('c')
        lat = kwargs['query'].get('lat')
        lon = kwargs['query'].get('lon')
        if lon and lat:
            location = Point(int(lon), int(lat), srid=4326)
        # import pdb; pdb.set_trace()
        data = self.filter(models.Q(name__icontains=q) | models.Q(description__icontains=q))

        if qc != 'all':
            return data.filter(category__slug=qc)
        if ql == 'nearby_store':
            return data.annotate(distance=Distance('location', location)).order_by('distance')
        else:
            return data

    
class AvailableProductManager(models.Manager):
    def get_queryset(self):
        return AvailableProductQuerySet(self.model, using=self._db)

    def available(self):
        return self.get_queryset().available()
    
    def get_interest_product(self, user_interest):
        return self.get_queryset().get_interest_product(user_interest)

    def filter_products(self, **kwargs):
        return self.get_queryset().filter_products(**kwargs)

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    store = models.ForeignKey(Store, related_name="store_product", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    description = models.TextField(blank=True)
    processing_time = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=60)
    location = models.PointField(null=True, blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    available_products = AvailableProductManager()

    class Meta:
        ordering = ('-created',)
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
    cancellation_reason = models.CharField(max_length=255, null=True, blank=True)
    quantity =models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-updated',)

    def __str__(self):
        return f'order of {self.product.name} from {self.user.first_name} to {self.store.name}'


    @classmethod
    def get_total_order_count(cls, request, **kwargs):
        return Order.objects.filter(**kwargs).count()

    @classmethod
    def get_awaiting_order_count(cls, request, **kwargs):
        return Order.objects.filter(**kwargs, status=cls.AWAITING).count()

    @classmethod
    def get_confirmed_order_count(cls, request, **kwargs):
        return Order.objects.filter(**kwargs, status=cls.CONFIRMED).count()

    @classmethod
    def get_cancelled_order_count(cls, request, **kwargs):
        return Order.objects.filter(**kwargs, status=cls.CANCELLED).count()

    @classmethod
    def get_delivered_order_count(cls, request, **kwargs):
        return Order.objects.filter(**kwargs, status=cls.DELIVERED).count()
    
    @classmethod
    def get_processing_order_count(cls, request, **kwargs):
        return Order.objects.filter(**kwargs, status=cls.PROCESSING).count()

    @classmethod
    def get_awaiting_order(cls, **kwargs):
        return Order.objects.filter(**kwargs, status=cls.AWAITING)

    @classmethod
    def get_confirmed_order(cls, **kwargs):
        return Order.objects.filter(**kwargs, status=cls.CONFIRMED)

    @classmethod
    def get_cancelled_order(cls, **kwargs):
        return Order.objects.filter(**kwargs, status=cls.CANCELLED)

    @classmethod
    def get_delivered_order(cls, **kwargs):
        return Order.objects.filter(**kwargs, status=cls.DELIVERED)
    
    @classmethod
    def get_processing_order(cls, **kwargs):
        return Order.objects.filter(**kwargs, status=cls.PROCESSING)

    def filter_order_based_on_query(request, **kwargs):
        query = request.GET.get('q')
        # import pdb; pdb.set_trace()
        if query == 'confirmed_order':
            queryset = Order.get_confirmed_order(**kwargs)
        elif query == 'cancelled_order':
            queryset = Order.get_cancelled_order(**kwargs)
        elif query == 'delivered_order':
            queryset = Order.get_delivered_order(**kwargs)
        elif query == 'processing_order':
            queryset = Order.get_processing_order(**kwargs)
        elif query == 'awaiting_order':
            queryset = Order.get_awaiting_order(**kwargs)
        else:
            queryset = Order.objects.filter(**kwargs)

        return queryset
