import operator
from functools import reduce

from django.db.models import Q
from rest_framework.generics import ListAPIView

from core.models import YTMetadata
from core.paginations import StandardResultsSetPagination
from core.serializers import YTMetadataSerializer


class SearchV1APIView(ListAPIView):
    serializer_class = YTMetadataSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        query = self.request.query_params.get("q", "")

        tokens = query.split()
        q_title_objects = [Q(title__icontains=token) for token in tokens]
        q_description_objects = [Q(description__icontains=token) for token in tokens]
        query = reduce(operator.or_, q_title_objects + q_description_objects)

        return YTMetadata.objects.filter(query).order_by("-published_at")
