
from rest_framework import serializers


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def validate_image(self, image):
        max_size = 10 * 1024 * 1024  # 10 MB

        if image.size > max_size:
            raise serializers.ValidationError(
                "Image size must not exceed 10 MB."
            )

        allowed_formats = {"JPEG", "PNG", "WEBP"}

        if image.image.format not in allowed_formats:
            raise serializers.ValidationError(
                "Only JPEG, PNG, and WEBP images are supported."
            )

        return image
