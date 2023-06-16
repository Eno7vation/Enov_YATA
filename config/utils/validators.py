from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
def validate_name(self):
    if (self.value > 5) | (self.value < 0 ):
        msg = u"input value 0~5"
        raise ValidationError(msg)

def validate_image_extension(value):
    ext = value.name.split('.')[-1]
    if ext.lower() not in ['jpg', 'jpeg', 'png']:
        raise ValidationError(
            _(f'지원하지 않는 파일포멧 : {ext}. 해당필드는 Image필드이므로, PNG와 JPG와 같은 확장자만 업로드할 수 있습니다.'),
            code='invalid_image_extension'
        )

@deconstructible
class MaxValueValidator(BaseValidator):
    message = _('이 값이 %(limit_value)보다 작거나 같아야합니다.')
    code = 'max_value'

    def compare(self, a, b):
        return a > b


@deconstructible
class MinValueValidator(BaseValidator):
    message = _('이 값이 %(limit_value)보다 크거나 같아야 합니다.')
    code = 'min_value'

    def compare(self, a, b):
        return a < b