
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ImageUploadSerializer


class ImageProcessView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image = serializer.validated_data["image"]

        return Response(
            {
                "success": True,
                "message": "Image uploaded and validated successfully.",
                "image": {
                    "filename": image.name,
                    "size_bytes": image.size,
                    "content_type": image.content_type,
                },
                "processing": {
                    "status": "pending",
                    "message": "AI processing will be implemented next.",
                },
            },
            status=status.HTTP_200_OK,
        )
