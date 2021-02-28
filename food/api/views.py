from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from ..models import Food
from .serializers import FoodSerializer


class FoodListCreateAPIView(ListCreateAPIView):
    queryset = Food.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = FoodSerializer


class FoodRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = FoodSerializer
