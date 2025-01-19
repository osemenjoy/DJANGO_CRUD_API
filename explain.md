# Django API Views Example

## Import Statements
```python
from django.http import JsonResponse
import json
from .models import Product
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductSerializer
from rest_framework import mixins, generics

def home(request):
    model_data = Product.objects.all().order_by("?").first()
    data = {}
    if model_data:
        data = model_to_dict(model_data, fields=["id", "title"])

    return JsonResponse(data)

@api_view(["GET"])
def api_home(request):
    model_data = Product.objects.all().order_by("?").first()
    data = {}
    if model_data:
        data = model_to_dict(model_data)
    return Response(data)

@api_view(["GET"])
def api_serialized_view(request):
    model_data = Product.objects.all().order_by("?").first()
    serialized_data = {}
    if model_data:
        serialized_data = ProductSerializer(model_data).data  # `.data` gives cleaned/validated data.
    return Response(serialized_data)

@api_view(["POST"])
def api_send(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):  # Raises exception if data is invalid
        validated_data = serializer.save()  # `.save` creates an instance in the database
        validated_data = serializer.data
        print(validated_data)
        return Response(validated_data)

@api_view(["GET", "POST"])
def product_alt_view(request, pk=None):
    method = request.method
    serializer = ProductSerializer(data=request.data)
    
    if method == "POST":  # Sending data to the database
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get("title")
            content = serializer.validated_data.get("content") or None
            if content is None:
                content = title
            serializer.save(content=content)  # Saves the instance with custom content
            validated_data = serializer.data
            return Response(validated_data)
        return Response({"message": "Product creation failed"}, status=400)
    
    if method == "GET":  # Fetching data
        if pk is not None:
            object = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(object).data
            return Response(data)
        
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data  # `many=True` for multiple objects
        return Response(data)

class ProductMixinView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, pk=None):
        if pk is not None:
            return self.retrieve(request)
        return self.list(request)
    
    def post(self, request):
        return self.create(request)
    
    def put(self, request, **kwargs):
        return self.update(request)
    
    def delete(self, request, pk=None):
        return self.destroy(request)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

# api view
class ProductListCreateAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

