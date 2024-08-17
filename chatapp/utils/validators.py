from django.core.validators import RegexValidator

PhoneNumberValidator = RegexValidator(
    regex="^09[1-3][0-9]{8}$",
    message="invalid phone number"
)
