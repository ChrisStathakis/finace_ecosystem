from django import forms
from portfolio.models import Ticker


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class TickerForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Ticker
        fields = ['title', "ticker", "indices"]

