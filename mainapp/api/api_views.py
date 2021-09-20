from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import ProductSerializer
from ..models import Product


class ProductAPIView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'

#class ServicePagination(PageNumberPagination):
#    """"""
#    page_size = 2
#    page_size_query_param = 'page_size'
#    max_page_size = 10
#
#    def get_paginated_response(self, data):
#        return Response(OrderedDict([
#            ('objects_count', self.page.paginator.count),
#            ('next', self.get_next_link()),
#            ('previous', self.get_previous_link()),
#            ('items', data)
#        ]))
#
#
#class ServiceListAPIView(ListAPIView):
#    """"""
#    serializer_class = ServiceSerializer
#    pagination_class = ServicePagination
#    queryset = Service.objects.all()
#    lookup_field = 'id'
#
#
#class ServiceAPIView(RetrieveAPIView, ListCreateAPIView, RetrieveUpdateAPIView):
#    """"""
#    serializer_class = ServiceSerializer
#    pagination_class = ServicePagination
#    queryset = Service.objects.all()
#    lookup_field = 'id'
#
#
#class PSListAPIView(ListAPIView):
#    serializer_class = PSSerializer
#    queryset = Product.objects.all()
#    filter_backends = [SearchFilter]
#    search_fields = ['price', 'title']
#
#
#class AccessorizeListAPIView(ListAPIView):
#    """"""
#    serializer_class = AccessorizeSerializer
#    queryset = Product.objects.all()
#    filter_backends = [SearchFilter]
#    search_fields = ['price', 'title']
#    #def get_queryset(self):
#    #    qs = super().get_queryset()
#    #    price, title = self.request.query_params.get('price'), self.request.query_params.get('title')
#    #    search_params = {'price__iexact': price, 'title__iexact': title}
#    #    return qs.filter(**search_params)
#
#
#class AccessorizeDetailAPIView(RetrieveAPIView):
#    """"""
#    serializer_class = AccessorizeSerializer
#    queryset = Product.objects.all()
#    lookup_field = 'id'
#
#
#class CustomersListAPIView(ListAPIView):
#    """"""
#    serializer_class = CustomerSerializer
#    queryset = Product.objects.all()