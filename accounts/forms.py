from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Address


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-600 focus:ring-2 focus:ring-indigo-100 outline-none transition',
        'placeholder': 'At least 6 characters'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-600 focus:ring-2 focus:ring-indigo-100 outline-none transition',
        'placeholder': 'Re-enter password'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-600 focus:ring-2 focus:ring-indigo-100 outline-none transition', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-600 focus:ring-2 focus:ring-indigo-100 outline-none transition', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-600 focus:ring-2 focus:ring-indigo-100 outline-none transition', 'placeholder': 'Choose username'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-indigo-600 focus:ring-2 focus:ring-indigo-100 outline-none transition', 'placeholder': 'name@example.com'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email address already exists.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none'}))

    class Meta:
        model = UserProfile
        fields = ['phone', 'bio']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none', 'placeholder': '+91 98765 43210'}),
            'bio': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none', 'rows': 3, 'placeholder': 'Tell us about yourself...'}),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'phone_number', 'street_address', 'apartment_suite', 'city', 'state', 'postal_code', 'country', 'address_type', 'is_default_shipping', 'delivery_instructions']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none', 'placeholder': 'Full Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none', 'placeholder': 'Phone Number for delivery contact'}),
            'street_address': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none', 'placeholder': 'Street address or P.O. Box'}),
            'apartment_suite': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none', 'placeholder': 'Apt, Suite, Unit, Building (optional)'}),
            'city': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none', 'placeholder': 'State / Province'}),
            'postal_code': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none', 'placeholder': 'ZIP / Postal Code'}),
            'country': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none', 'placeholder': 'Country'}),
            'address_type': forms.Select(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none bg-white'}),
            'delivery_instructions': forms.Textarea(attrs={'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-indigo-600 outline-none', 'rows': 2, 'placeholder': 'e.g. Leave at front door, gate code #1234'}),
            'is_default_shipping': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-indigo-600 rounded border-slate-300 focus:ring-indigo-500'}),
        }
