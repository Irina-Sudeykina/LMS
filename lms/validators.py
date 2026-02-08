from rest_framework.serializers import ValidationError

def validate_url_source(value):
    if "youtube.com" not in value.lower():
        raise ValidationError("Ипользован запрещенный ресурс")
