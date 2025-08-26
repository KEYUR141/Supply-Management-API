from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, Vendor, Warehouse, Product, Stock, StockTransfer

# ----------------------------
# User & Profile Serializers
# ----------------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.CharField(write_only=True, required=False)  # vendor, incharge, admin

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'password2', 'role')
        read_only_fields = ('id',)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        role = validated_data.pop('role', 'vendor')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Create or update UserProfile
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.role = role
        profile.save()
                        
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = UserProfile
        fields = ["uuid", "user", "role", "first_name", "last_name", "username"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

# ----------------------------
# Vendor Serializer
# ----------------------------
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['uuid', 'name', 'contact_email', 'phone', 'address']


# ----------------------------
# Warehouse Serializer
# ----------------------------
class WarehouseSerializer(serializers.ModelSerializer):
    incharge = UserProfileSerializer(read_only=True)
    incharge_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        source='incharge',
        write_only=True
    )

    class Meta:
        model = Warehouse
        fields = ['uuid', 'name', 'location', 'incharge', 'incharge_id']

    def validate_incharge(self, value):
        if value and value.role not in ["admin", "Warehouse-Incharge"]:
            raise serializers.ValidationError(
                "Incharge must be an admin or a Warehouse-Incharge."
            )
        return value

# ----------------------------
# Product Serializer
# ----------------------------
class ProductSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)
    vendor_id = serializers.PrimaryKeyRelatedField(
        queryset=Vendor.objects.all(),
        source='vendor',
        write_only=True
    )

    class Meta:
        model = Product
        fields = ['uuid', 'product_id', 'name', 'description', 'sku', 'barcode', 'vendor', 'vendor_id']


# ----------------------------
# Stock Serializer
# ----------------------------
class StockSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    warehouse = WarehouseSerializer(read_only=True)
    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(),
        source='warehouse',
        write_only=True
    )

    class Meta:
        model = Stock
        fields = ['uuid', 'product', 'product_id', 'warehouse', 'warehouse_id', 'quantity']


# ----------------------------
# Stock Transfer Serializer
# ----------------------------
class StockTransferSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    from_warehouse = WarehouseSerializer(read_only=True)
    from_warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(),
        source='from_warehouse',
        write_only=True
    )

    to_warehouse = WarehouseSerializer(read_only=True)
    to_warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(),
        source='to_warehouse',
        write_only=True
    )

    class Meta:
        model = StockTransfer
        fields = [
            'id', 'product', 'product_id',
            'from_warehouse', 'from_warehouse_id',
            'to_warehouse', 'to_warehouse_id',
            'quantity', 'transfer_date'
        ]
