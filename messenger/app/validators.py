from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _('Parol kamida 8 ta belgidan iborat bo\'lishi kerak.'),
                code='password_too_short',
            )

    def get_help_text(self):
        return _(
            'Parol kamida 8 ta belgidan iborat bo\'lishi kerak va foydalanuvchi nomiga o\'xshash bo\'lmasligi kerak.'
        )