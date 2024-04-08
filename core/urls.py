from django.urls import path

from core.views import SearchV1APIView

urlpatterns = [
    path("v1/search", SearchV1APIView.as_view(), name="v1_search"),
]
