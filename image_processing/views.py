import os
import tempfile

from paddleocr import PaddleOCR
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ImageUploadSerializer


ocr = PaddleOCR(
    lang="en",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)


class ImageProcessView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image = serializer.validated_data["image"]
        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                suffix=".jpg", delete=False
            ) as temp:
                temp_path = temp.name

                for chunk in image.chunks():
                    temp.write(chunk)

            # The file is now closed, so Windows can read it.
            result = ocr.predict(temp_path)

            extracted_text = []
            for page in result:
                extracted_text.extend(page["rec_texts"])

            return Response(
                {
                    "success": True,
                    "message": "Image processed successfully.",
                    "image": {
                        "filename": image.name,
                        "size_bytes": image.size,
                        "content_type": image.content_type,
                    },
                    "processing": {
                        "status": "completed",
                        "extracted_text": extracted_text,
                        "message": "Text extraction finished.",
                    },
                },
                status=status.HTTP_200_OK,
            )
        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)