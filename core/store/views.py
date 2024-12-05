from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from .models import Product, Cart, CartItem, Category, ProductImageUpload, ProductImage
from . import serializers
from .filters import ProductsFilter, CategoryFilter


class CategoryView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        filterset = CategoryFilter(request.GET, queryset=Category.objects.all().order_by('id'))
        category_count = filterset.qs.count()

        # Pagination ///////////////////////
        resPerPage = 20
        paginator = PageNumberPagination()
        paginator.page_size = resPerPage
        queryset = paginator.paginate_queryset(filterset.qs, request)

        serializer = serializers.CategorySerializer(queryset, many=True)
        return Response({
            'categoryCount': category_count,
            'resPerpage': resPerPage,
            'Categories': serializer.data
        })


# Products Views ////////////////
class ProductCreateListView(APIView):
    """
    Retrieve a list of all products or add a new product (admin functionality).
    """
    def get_permissions(self):
        # Allow any unauthenticated user access
        if self.request.method == 'GET':
            return [permissions.AllowAny()]

        # Restrict access to admin users only
        elif self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def get(self, request):
        filterset = ProductsFilter(request.GET, queryset=Product.objects.all().order_by('id'))
        product_count = filterset.qs.count()

        # Pagination ///////////////////////
        resPerPage = 50
        paginator = PageNumberPagination()
        paginator.page_size = resPerPage
        queryset = paginator.paginate_queryset(filterset.qs, request)

        serializer = serializers.ProductSerializer(queryset, many=True)
        return Response({
            'productCount': product_count,
            'resPerpage': resPerPage,
            'Products': serializer.data
        })

    def post(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Only admins can add products.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.ProductSerializer(data=request.data)

        if serializer.is_valid():
            image_urls = serializer.validated_data.pop('image_urls', [])

            product_name = serializer.validated_data['name']

            if Product.objects.filter(name=product_name).exists():
                return Response({'error': 'A product with same details exists, please choose another name'}, status=status.HTTP_400_BAD_REQUEST)

            product = serializer.save()

            for image in image_urls:
                ProductImage.objects.create(product=product, image=image)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    """
    Retrieve, update, or delete a specific product by ID (admin functionality for PUT and DELETE).
    """

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        elif self.request.method in ['POST', 'PUT', 'PATCH']:
            return [permissions.IsAdminUser()]

        return super().get_permissions()

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = serializers.ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        if not request.user.is_staff:
            return Response({'error': 'Only admins can update products.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            product = Product.objects.get(pk=pk)
            serializer = serializers.ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response({'error': 'Only admins can delete products.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response({'message': 'Product deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_200_OK)


class UploadProductImagesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = serializers.CreaeteProductImageUploadSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        images = serializer.validated_data["images"]

        product_images_list = []
        for image in images:
            product_image = ProductImageUpload.objects.create(
                image=image,
            )

            product_images_list.append(product_image)

        serializer = serializers.ProductImageSerializer(
            product_images_list, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Cart Views
class CartView(APIView):
    """
    Retrieve the current state of the shopping cart or add a product to the cart.
    """

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        elif self.request.method in ['POST', 'DELETE']:
            return [permissions.IsAuthenticated()]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)

        if not cart.items.exists():
            return Response({'response': 'Shopping cart is empty'}, status=status.HTTP_200_OK)

        serializer = serializers.CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        products = request.data.get("products", [])

        if not isinstance(products, list) or not products:
            return Response(
                {"error": "Products must be a non-empty list."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get or create the user's cart
        cart, _ = Cart.objects.get_or_create(user=user)

        cart_items_response = []
        for product_data in products:
            product_id = product_data.get("product")
            quantity = product_data.get("quantity", 1)

            if not product_id:
                return Response(
                    {"error": "Each product must have a valid product ID."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if the product exists
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the product already exists in the cart
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            if created:
                # If a new CartItem was created, set its quantity
                cart_item.quantity = quantity
            else:
                # If the CartItem exists, update the quantity
                cart_item.quantity += int(quantity)

            cart_item.save()
            cart_items_response.append(serializers.CartItemSerializer(cart_item).data)

        return Response(
            {"cart_items": cart_items_response},
            status=status.HTTP_201_CREATED,
        )


class CartItemView(APIView):
    """
    Update the quantity of a product in the cart or remove a product from the cart.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            cart_item = CartItem.objects.get(pk=pk, cart__user=request.user)
            serializer = serializers.CartItemSerializer(cart_item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            cart_item = CartItem.objects.get(pk=pk, cart__user=request.user)
            cart_item.delete()
            return Response({'message': 'Item removed from cart.'}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)
