from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import Consumer, StatusChoices
from .serializers import ConsumerBulkCreateSerializer, ConsumerSerializer


class ConsumerFilter(filters.FilterSet):

    min_balance = filters.NumberFilter(field_name="balance", lookup_expr="gte")
    max_balance = filters.NumberFilter(field_name="balance", lookup_expr="lte")
    consumer_name = filters.CharFilter(
        field_name="consumer_name", lookup_expr="icontains"
    )
    status = filters.ChoiceFilter(field_name="status", choices=StatusChoices.choices)

    class Meta:
        model = Consumer
        fields = ("balance", "status", "consumer_name")


class ConsumerCreateListAPIView(ListAPIView):

    serializer_class = ConsumerSerializer
    queryset = Consumer.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ConsumerFilter

    def post(self, request, *args, **kwargs):
        serializer = ConsumerBulkCreateSerializer(data=request.data)

        data = {"error": "invalid file"}
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()

        return Response(data=data, status=201)
