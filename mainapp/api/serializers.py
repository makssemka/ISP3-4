from rest_framework import serializers

from ..models import Service, Product


from rest_framework import serializers

from ..models import Service, Product, Customer, Order


class ProductSerializer(serializers.ModelSerializer):
    """"""
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects)
    title = serializers.CharField(required=True)
    slug = serializers.SlugField(required=True)
    image = serializers.ImageField(required=True)
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=9, decimal_places=2, required=True)

    class Meta:
        model = Product
        fields = '__all__'


#class PSSerializer(BaseProductSerializer, serializers.ModelSerializer):
#    """"""
#    diagonal = serializers.CharField(required=True)
#    display = serializers.CharField(required=True)
#    proccesor_freq = serializers.CharField(required=True)
#
#    class Meta:
#        model = Product
#        fields = '__all__'
#
#
#class AccessorizeSerializer(BaseProductSerializer, serializers.ModelSerializer):
#    """"""
#    diagonal = serializers.CharField(required=True)
#    display = serializers.CharField(required=True)
#    proccesor_freq = serializers.CharField(required=True)
#
#    class Meta:
#        model = Product
#        fields = '__all__'
#
#
#class OrderSerializer(serializers.ModelSerializer):
#    """"""
#    class Meta:
#        model = Order
#        fields = '__all__'
#
#
#class CustomerSerializer(serializers.ModelSerializer):
#    """"""
#    orders = OrderSerializer(many=True)
#
#    class Meta:
#        model = Customer
#        fields = '__all__'
