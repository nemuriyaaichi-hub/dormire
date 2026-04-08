import base64
import uuid

import six
from django.core.files.base import ContentFile
from rest_framework.serializers import ImageField, ModelSerializer

from .models import Measure, MeasureOnly


class Base64ImageField(ImageField):
    def to_internal_value(self, data):

        if isinstance(data, six.string_types):
            if "data:" in data and ";base64," in data:
                header, data = data.split(";base64,")

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail("invalid_image")

            file_name = str(uuid.uuid4())
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (
                file_name,
                file_extension,
            )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super().to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class MeasureSerializer(ModelSerializer):
    image1 = Base64ImageField(use_url=True, required=False)
    image2 = Base64ImageField(use_url=True, required=False)

    class Meta:
        model = Measure
        exclude = (
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "user")


class MeasureOnlySerializer(ModelSerializer):
    image1 = Base64ImageField(use_url=True, required=False)
    image2 = Base64ImageField(use_url=True, required=False)

    class Meta:
        model = MeasureOnly
        exclude = (
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "user")
