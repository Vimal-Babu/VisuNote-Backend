
from django.urls import path

from .views import ImageProcessView

urlpatterns = [
    path("process/",ImageProcessView.as_view(),name="image-process",),
]
