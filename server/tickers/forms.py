from django import forms
from .models import Portfolio, UserTicker


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class PortfolioBaseForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Portfolio
        fields = ['title', 'user', ]


class UserTickerForm(BaseForm, forms.ModelForm):

    class Meta:
        model = UserTicker
        fields = ['ticker', 'portfolio', 'starting_investment', 'starting_value_of_ticker']
        widgets = {'ticker': forms.HiddenInput(), 'portfolio': forms.HiddenInput()}