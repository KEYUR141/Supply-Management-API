from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True

class UserProfile(BaseModel):
    role_choices = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
        ('incharge', 'Warehouse-Incharge'),
        ('vendor', 'Vendor'),
        ('auditor', 'Auditor'),
    )
    
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=20,choices=role_choices,default='employee')
    #profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)  # <-- added field

    def __str__(self):
        return f"{self.uuid} - {self.user.username} - {self.role}"
    

class Warehouse(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255)
    incharge = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'incharge'})

    def __str__(self):
        return f"{self.uuid} - {self.name} - {self.location} - {self.incharge}"

class Vendor(BaseModel):
    VENDOR_TYPE_CHOICES = (
        ('freelancer', 'Freelancer'),
        ('wholesaler', 'Wholesaler'),
        ('organization', 'Organization'),
    )
    name = models.CharField(max_length=100, unique=True)
    contact_email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    vendor_type = models.CharField(max_length=20, choices=VENDOR_TYPE_CHOICES, default='organization')

    def __str__(self):
        return self.name
    

class Product(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=50, unique=True)  # Stock Keeping Unit
    barcode = models.CharField(max_length=100, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
    product_id = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not hasattr(self, 'product_id') or not self.product_id:
            # Find the last product_id in the DB and increment
            last_product = Product.objects.order_by('-created_at').first()
            if last_product and hasattr(last_product, 'product_id') and last_product.product_id and last_product.product_id.startswith("PROD-"):
                try:
                    last_num = int(last_product.product_id.split('-')[1])
                except (IndexError, ValueError):
                    last_num = 0
                self.product_id = f"PROD-{last_num + 1:04d}"
            else:
                self.product_id = "PROD-0001"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.product_id})"



class Stock(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stocks')
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'warehouse')

    def __str__(self):
        return f"{self.product.product_id} - {self.warehouse.name} - {self.quantity}"



class StockTransfer(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    from_warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name='outgoing_transfers'
    )
    to_warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name='incoming_transfers'
    )
    quantity = models.PositiveIntegerField()
    transfer_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer {self.product.product_id} from {self.from_warehouse} to {self.to_warehouse}"


