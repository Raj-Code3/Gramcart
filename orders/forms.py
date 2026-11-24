from django import forms
from .models import Order

class CheckoutForm(forms.Form):
    # Shipping details
    full_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none text-slate-800 font-medium',
        'placeholder': 'First & Last Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none text-slate-800 font-medium',
        'placeholder': 'name@example.com'
    }))
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none text-slate-800 font-medium',
        'placeholder': '+91 98765 43210'
    }))
    shipping_address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none text-slate-800 font-medium',
        'placeholder': 'Street address, P.O. box, company'
    }))
    apartment_suite = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none text-slate-800 font-medium',
        'placeholder': 'Apt, Suite, Unit, Building (optional)'
    }))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none text-slate-800 font-medium',
        'placeholder': 'City'
    }))
    state = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none text-slate-800 font-medium',
        'placeholder': 'State / Province'
    }))
    postal_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none text-slate-800 font-medium',
        'placeholder': '6-digit PIN Code'
    }))
    def clean_postal_code(self):
        import re
        pin = self.cleaned_data['postal_code'].strip()
        if not re.fullmatch(r'[1-9][0-9]{5}', pin):
            raise forms.ValidationError('Enter a valid 6-digit Indian PIN code.')
        return pin

    def clean_country(self):
        return 'India'

    country = forms.CharField(max_length=100, initial='India', widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none text-slate-800 font-medium',
        'placeholder': 'Country'
    }))

    # Delivery & Payment selections
    delivery_method = forms.ChoiceField(
        choices=Order.DELIVERY_METHOD_CHOICES,
        initial='standard',
        widget=forms.RadioSelect(attrs={'class': 'delivery-method-radio'})
    )
    payment_method = forms.ChoiceField(
        choices=Order.PAYMENT_METHOD_CHOICES,
        initial='card',
        widget=forms.RadioSelect(attrs={'class': 'payment-method-radio'})
    )
    
    # Mock card details
    card_number = forms.CharField(required=False, max_length=19, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none font-mono',
        'placeholder': '•••• •••• •••• ••••'
    }))
    card_expiry = forms.CharField(required=False, max_length=5, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none font-mono',
        'placeholder': 'MM/YY'
    }))
    card_cvv = forms.CharField(required=False, max_length=4, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none font-mono',
        'placeholder': 'CVC'
    }))
    
    delivery_notes = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none text-slate-800',
        'rows': 2,
        'placeholder': 'e.g. Leave package by side porch, gate passcode'
    }))
    save_address = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={
        'class': 'w-4 h-4 text-indigo-600 rounded border-slate-300 focus:ring-indigo-500'
    }))
