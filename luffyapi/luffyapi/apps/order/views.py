from rest_framework.generics import CreateAPIView
from .models import Order,OrderDetail
from .serializers import OrderModelSerializer
class OrderAPIView(CreateAPIView):
    queryset = Order.objects.filter(is_delete=False, is_show=True)
    serializer_class = OrderModelSerializer
