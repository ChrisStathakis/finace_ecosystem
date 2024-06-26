from django.conf import settings
from django import forms

def site_settings(request):
    currency = settings.CURRENCY
    return {'currency': currency}


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'