from django import forms
from .models import Sale

class RefundForm(forms.Form):
    sale_id = forms.IntegerField()
    refund_amount = forms.DecimalField(decimal_places=2, max_digits=10)

    def clean_sale_id(self):
        sale_id = self.cleaned_data['sale_id']
        if not Sale.objects.filter(id=sale_id).exists():
            raise forms.ValidationError('Sale does not exist.')
        return sale_id

    def clean_refund_amount(self):
        amount = self.cleaned_data['refund_amount']
        if amount <= 0:
            raise forms.ValidationError('Refund amount must be positive.')
        return amount

class CreateSaleForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1)
