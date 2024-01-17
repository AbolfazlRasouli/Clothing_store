from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def validate_image(value):
    if value.width != value.height:
        raise ValidationError(
                         _('image : the image must be square ')
                    )


def validate_birthday(value):
    if value and value > timezone.now().date():
        raise ValidationError(
             _('birthday : Birthdate cannot be in the future ')
        )

# birthday_validator = MaxValueValidator(limit_value=timezone.now().today(),
#                                        message=_('birthday : Birthdate cannot be in the future '))
