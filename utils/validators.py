from django.core.validators import RegexValidator


class SKUValidator(RegexValidator):
    regex = r'^[a-zA-Z0-9\-]{6,20}$'
    message = "SKU must be alphanumeric with 6 to 20 characters"
    code = "invalid _sku"


class PhoneNumberValidator(RegexValidator):
    regex = r'^98(9[0-3,9]\d{8}|[1-9]\d{9})$'
    message = 'phone number must be valid 12 digits like 98xxxxxxxxxxx'
    code = 'invalid _phone_number'


phone_number_validator = PhoneNumberValidator()
sku_validator = SKUValidator()
