from django.core.exceptions import ValidationError


def validate_image_extension(value):
    if not value.name.lower().endswith((".jpg", ".jpeg", ".png")):
        raise ValidationError("File must be a jpeg or png image.")
