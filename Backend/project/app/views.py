from django.shortcuts import render
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ProductSerializer, UserSerializer, WarehouseSerializer, UserProfileSerializer, VendorSerializer, StockSerializer, StockTransferSerializer
from .models import UserProfile, Warehouse, Vendor, Product, Stock, StockTransfer
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - Admins can create/update/delete
    - Others can only view (GET, HEAD, OPTIONS)
    """
    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only allow write/delete for admin
        if request.user and request.user.is_authenticated:
            profile = getattr(request.user, "userprofile", None)
            if profile and profile.role in ["admin", "Admin"]:
                return True
        return False

class AuthViewSet(viewsets.ViewSet):
    """
    ViewSet for user registration and login with error handling.
    """
    @action(detail=False, methods=['get'])
    @permission_classes([IsAuthenticated])
    def get_user(self, request):
        try:
            user = request.user
            if user.is_authenticated:
                user_profile = UserProfile.objects.all()
                serializer = UserProfileSerializer(user_profile, many=True)
                return Response({
                    "Status": True,
                    "Method":"Get",
                    "Data": serializer.data
                })
            return Response({
                "Status": False,
                "Method":"Get",
                "Data": "User not authenticated"
            })
        except Exception as e:
            return Response({
                "Status": False,
                "Method":"Get",
                "Data": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def register(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()

                # Generate JWT token for newly registered user
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "User registered successfully",
                    "user": UserSerializer(user).data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "error": "Registration failed",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def login(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")

            if not username or not password:
                return Response({"error": "Username and password are required"},
                                status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "Login successful",
                    "user": UserSerializer(user).data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=status.HTTP_200_OK)

            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({
                "error": "Login failed",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAdminOrReadOnly]
    # permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def get(self, request):
        try:
            warehouses = self.queryset
            serializer = self.serializer_class(warehouses, many=True)
            return Response({
                'status': True,
                'Method': request.method,
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'status': False,
                'Method': request.method,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True,methods=['post'])
    def post(self, request, pk=None):
        try:
            serializer = self.serializer_class(data=request.data)
            if(serializer.is_valid()):
                serializer.save()
                return Response({
                    'status': True,
                    'Method': request.method,
                    'data': serializer.data
                })
            else:
                return Response({
                    'status': False,
                    'Method': request.method,
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status': False,
                'Method': request.method,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    
    @action(detail=False,methods=['PATCH'])
    def patch(self, request):
        try:
            updates = request.data.get('updates')
            if not updates:
                return Response({'STATUS': False, 'Message': 'No updates provided'}, status=status.HTTP_400_BAD_REQUEST)
            updated_Warehouses = []
            Errors = []
            for update in updates:
                if not isinstance(update, dict):
                    Errors.append({'error': 'Each update must be a dictionary'})
                    continue
                uid = update.get('uuid')
                if not uid:
                    Errors.append({'uuid': None, 'error': 'UUID is required'})
                    continue
                try:
                    obj = Warehouse.objects.get(uuid=uid)
                    serializer = self.serializer_class(obj, data=update, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        updated_Warehouses.append(serializer.data)
                    else:
                        Errors.append({'uuid': uid, 'error': serializer.errors})
                except Warehouse.DoesNotExist:
                    Errors.append({'uuid': uid, 'error': 'Warehouse does not exist'})
            return Response({
                'STATUS': True,
                'Message': 'Warehouse data is updated',
                'Data': updated_Warehouses,
                'Errors': Errors
            })
        except Exception as e:
            return Response({
                'STATUS': False,
                'Message': 'Error Occured',
                'Error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False,methods=['DELETE'])
    def delete(self, request):
        try:
            deletes = request.data.get('deletes')
            if not deletes:
                return Response({'STATUS': False, 'Message': 'No deletes provided'}, status=status.HTTP_400_BAD_REQUEST)
            deleted_Warehouses = []
            Errors = []
            for delete in deletes:
                if not isinstance(delete, dict):
                    Errors.append({'error': 'Each delete must be a dictionary'})
                    continue
                uid = delete.get('uuid')
                if not uid:
                    Errors.append({'uuid': None, 'error': 'UUID is required'})
                    continue
                try:
                    obj = Warehouse.objects.get(uuid=uid)
                    obj.delete()
                    deleted_Warehouses.append({'uuid': uid, 'message': 'Deleted'})
                    
                except Warehouse.DoesNotExist:
                    Errors.append({'uuid': uid, 'error': 'Warehouse does not exist'})
            return Response({
                'STATUS': True,
                'Message': 'Warehouse data is deleted',
                'Data': deleted_Warehouses,
                'Errors': Errors
            })
        except Exception as e:
            return Response({
                'STATUS': False,
                'Message': 'Error Occured',
                'Error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
class VendorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @action(detail=False, methods=['get'])
    def get(self,request):
        try:
            vendors = self.queryset
            serializer = self.serializer_class(vendors,many=True)
            return Response({
                'status': True,
                'Method': request.method,
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'status': False,
                'Method': request.method,
                'Error': str(e)
            })
    
    @action(detail=False, methods=['post'])
    def post(self,request):
        try:
            data = request.data
            if not isinstance(data, list) or not data:
                return Response({
                    'status': False,
                    'Method': request.method,
                    'Error': 'Data must be required'
                })
            serializer = self.serializer_class(data,data,many=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': True,
                    'Method': request.method,
                    'data': serializer.data
                })
            return Response({
                'status': False,
                'Method': request.method,
                'Error': serializer.errors
            })
        except Exception as e:
            return Response({
                'status': False,
                'Method': request.method,
                'Error': str(e)
            })

    @action(detail=False,methods=['PATCH'])
    def patch(self,request):
        try:
            updates = request.data.get('updates')
            if not updates:
                return Response({'STATUS': False, 'Message': 'No updates provided'}, status=status.HTTP_400_BAD_REQUEST)
            updated_Vendors = []
            Errors = []
            for update in updates:
                if not isinstance(update, dict):
                    Errors.append({'error': 'Each update must be a dictionary'})
                    continue
                uid = update.get('uuid')
                if not uid:
                    Errors.append({'uuid': None, 'error': 'UUID is required'})
                    continue
                try:
                    obj = Vendor.objects.get(uuid=uid)
                    serializer = self.serializer_class(obj, data=update, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        updated_Vendors.append(serializer.data)
                    else:
                        Errors.append({'uuid': uid, 'error': serializer.errors})
                except Vendor.DoesNotExist:
                    Errors.append({'uuid': uid, 'error': 'Vendor does not exist'})
            return Response({
                'STATUS': True,
                'Message': 'Vendor data is updated',
                'Data': updated_Vendors,
                'Errors': Errors
            })
        except Exception as e:
            return Response({
                'STATUS': False,
                'Message': 'Error Occured',
                'Error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False,methods=['DELETE'])
    def delete(self, request):
        try:
            deletes = request.data.get('deletes')
            if not deletes:
                return Response({'STATUS': False, 'Message': 'No deletes provided'}, status=status.HTTP_400_BAD_REQUEST)
            deleted_Vendors = []
            Errors = []
            for delete in deletes:
                if not isinstance(delete, dict):
                    Errors.append({'error': 'Each delete must be a dictionary'})
                    continue
                uid = delete.get('uuid')
                if not uid:
                    Errors.append({'uuid': None, 'error': 'UUID is required'})
                    continue
                try:
                    obj = Vendor.objects.get(uuid=uid)
                    obj.delete()
                    deleted_Vendors.append({'uuid': uid, 'message': 'Deleted'})
                    
                except Vendor.DoesNotExist:
                    Errors.append({'uuid': uid, 'error': 'Vendor does not exist'})
            return Response({
                'STATUS': True,
                'Message': 'Vendor data is deleted',
                'Data': deleted_Vendors,
                'Errors': Errors
            })
        except Exception as e:
            return Response({
                'STATUS': False,
                'Message': 'Error Occured',
                'Error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False,methods=['GET'])
    def get(self,request):
        try:
            products = self.queryset
            serializer = self.serializer_class(products, many=True)
            return Response({
                'STATUS': True,
                'Message': 'Product data retrieved successfully',
                'Data': serializer.data
            })
        except Exception as e:
            return Response({
                'STATUS': False,
                'Message': 'Error Occured',
                'Error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False,methods=['POST'])
    def post(self, request):
        try:
            data = request.data
            if not data or not isinstance(data, list):
                return Response({
                    'STATUS': False,
                    'Message': 'Data must be provided as a list'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = self.serializer_class(data=data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'STATUS': True,
                    'Message': 'Product data created successfully',
                    'Data': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'STATUS': False,
                'Message': 'Error Occured',
                'Error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'STATUS': False,
                'Message': 'Error Occured',
                'Error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,methods=['PATCH'])
    def patch(self,request):
        try:
            data = request.data.get('updates')
            if not data or not isinstance(data,list):
                return Response({
                    'STATUS': False,
                    'Message': 'Updates must be provided as a list'
                }, status=status.HTTP_400_BAD_REQUEST)
            updated_Products = []
            Errors = []
            for update in data:
                if not isinstance(update, dict):
                    Errors.append({'error': 'Each update must be a dictionary'})
                    continue
                uid = update.get('uuid')
                if not uid:
                    Errors.append({'uuid': None, 'error': 'UUID is required'})
                    continue
                try:
                    obj = Product.objects.get(uuid=uid)
                    serializer = self.serializer_class(obj, data=update, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        updated_Products.append({'uuid': uid, 'message': 'Updated'})
                    else:
                        Errors.append({'uuid': uid, 'error': serializer.errors})
                except Product.DoesNotExist:
                    Errors.append({'uuid': uid, 'error': 'Product does not exist'})
            return Response({
                'STATUS': True,
                'Message': 'Product data is updated',
                'Data': updated_Products,
                'Errors': Errors
            })
        except Exception as e:
            return Response({
                'STATUS': False,
                'Message': 'Error Occured',
                'Error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False,methods=['DELETE'])
    def delete(self,request):
        try:
            deletes = request.data.get('deletes')
            if not deletes or not isinstance(deletes, list):
                return Response({
                    'STATUS': False,
                    'Message': 'Deletes must be provided as a list'
                }, status=status.HTTP_400_BAD_REQUEST)

            deleted_Products = []
            Errors = []
            for delete in deletes:
                if not isinstance(delete, dict):
                    Errors.append({'error': 'Each delete must be a dictionary'})
                    continue
                uid = delete.get('uuid')
                if not uid:
                    Errors.append({'uuid': None, 'error': 'UUID is required'})
                    continue
                try:
                    obj = Product.objects.get(uuid=uid)
                    obj.delete()
                    deleted_Products.append({'uuid': uid, 'message': 'Deleted'})
                except Product.DoesNotExist:
                    Errors.append({'uuid': uid, 'error': 'Product does not exist'})
            return Response({
                'STATUS': True,
                'Message': 'Product data is deleted',
                'Data': deleted_Products,
                'Errors': Errors
            })
        except Exception as e:
            return Response({
                'STATUS': False,
                'Message': 'Error Occured',
                'Error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
class StockViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = StockSerializer
    queryset = Stock.objects.all()

    @action(detail=False, methods=['get'])
    def get(self,request):
        try:
            stocks = self.queryset
            serializer = self.serializer_class(stocks, many=True)
            return Response({
                'STATUS': True,
                'Message': 'Stock data retrieved successfully',
                'Data': serializer.data
            })
        except Exception as e:
            return Response({
                'STATUS': False,
                'Message': 'Error Occured',
                'Error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def post(self,request):
        try:
            data = request.data
            if not data or not isinstance(data, list):
                return Response({
                    'STATUS': False,
                    'Message': 'Data must be provided as a list'
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.serializer_class(data=data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'STATUS': True,
                    'Message': 'Stock data created successfully',
                    'Data': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'STATUS': False,
                'Message': 'Error Occured',
                'Error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'STATUS': False,
                'Message': 'Error Occured',
                'Error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['PATCH'])
    def patch(self,request):
        try:
            updates = request.data.get('updates')
            if not updates or not isinstance(updates, list):
                return Response({
                    'STATUS': False,
                    'Message': 'Data must be provided as a list'
                }, status=status.HTTP_400_BAD_REQUEST)

            updated_stocks = []
            errors = []
            for item in updates:
                uid = item.get('uuid')
                if not uid:
                    errors.append({'uuid': None, 'error': 'UUID is required'})
                    continue
                try:
                    stock = Stock.objects.get(uuid=uid)
                    serializer = self.serializer_class(stock, data=item, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        updated_stocks.append(serializer.data)
                    else:
                        errors.append({'uuid': uid, 'error': serializer.errors})
                except Stock.DoesNotExist:
                    errors.append({'uuid': uid, 'error': 'Stock does not exist'})

            return Response({
                'STATUS': True,
                'Message': 'Stock data updated successfully',
                'Data': updated_stocks,
                'Errors': errors
            })
        except Exception as e:
            return Response({
                'STATUS': False,
                'Message': 'Error Occured',
                'Error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['DELETE'])
    def delete(self, request):
        try:
            deletes = request.data.get('deletes')
            if not deletes or not isinstance(deletes, list):
                return Response({
                    'STATUS': False,
                    'Message': 'Deletes must be provided as a list'
                }, status=status.HTTP_400_BAD_REQUEST)
            deleted_stocks = []
            errors = []
            for item in deletes:
                # Support both {'uuid': ...}, {'uid': ...}, and plain uuid string
                if isinstance(item, dict):
                    uid = item.get('uuid') or item.get('uid')
                else:
                    uid = item
                if not uid:
                    errors.append({'uuid': None, 'error': 'UUID is required'})
                    continue
                try:
                    stock = Stock.objects.get(uuid=uid)
                    stock.delete()
                    deleted_stocks.append(uid)
                except Stock.DoesNotExist:
                    errors.append({'uuid': uid, 'error': 'Stock does not exist'})

            return Response({
                'STATUS': True,
                'Message': 'Stock data deleted successfully',
                'Data': deleted_stocks,
                'Errors': errors
            })
        except Exception as e:
            return Response({
                'STATUS': False,
                'Message': 'Error Occured',
                'Error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class StockTransferViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = StockTransferSerializer
    queryset = StockTransfer.objects.all()

    @action(detail=False, methods=['get'])
    def get(self, request):
        try:
            data = request.data.get('data')
            if not data or not isinstance(data, list):
                return Response({
                    'STATUS': False,
                    'Message': 'Data must be provided as a list'
                }, status=status.HTTP_400_BAD_REQUEST)
            queryset = self.queryset
            serializer = self.serializer_class(queryset, many=True)
            return Response({
                'STATUS': True,
                'Message': 'Stock transfer data retrieved successfully',
                'Data': serializer.data
            })
        except Exception as e:
            return Response({
                'STATUS': False,
                'Message': 'Error Occured',
                'Error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
