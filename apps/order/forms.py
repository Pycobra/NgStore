from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm


from .models import Address



class UserAddressForm(forms.ModelForm):
    full_name = forms.CharField(label='Fullname', min_length=2, max_length=100, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'fullname'}))
    phone = forms.CharField(label='Phone', min_length=7, max_length=25, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'phone'}))
    address_line1 = forms.CharField(label='Address', min_length=10, max_length=250, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'address1'}))
    address_line2 = forms.CharField(label='Address2', min_length=10, max_length=250, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'address2'}))
    email = forms.EmailField(label='Email', min_length=2, max_length=250, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'email'}))
    city = forms.CharField(label='Town/City', min_length=2, max_length=250, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'city'}))
    postal_code = forms.CharField(label='Postcode', min_length=2, max_length=20, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'postal code'}))


    class Meta:
        model = Address
        fields = ["full_name", "phone", "email", "address_line1", "address_line2", "city", "postal_code"]




class UserEditAddressForm(forms.ModelForm):
    full_name = forms.CharField(label='Fullname', min_length=2, max_length=100, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'fullname'}))
    phone = forms.CharField(label='Phone', min_length=7, max_length=25, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'phone'}))
    address_line1 = forms.CharField(label='Address', min_length=10, max_length=250, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'address1'}))
    address_line2 = forms.CharField(label='Address2', min_length=10, max_length=250, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'address2'}))
    email = forms.EmailField(label='Email', min_length=2, max_length=250, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'email'}))
    city = forms.CharField(label='Town/City', min_length=2, max_length=250, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'city'}))
    postal_code = forms.CharField(label='Postcode', min_length=2, max_length=20, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'postal code'}))

    class Meta:
        model= Address
        fields=('full_name', 'city', 'phone', 'email', 'postal_code', 'address_line1', 'address_line2')

    def clean_address_line1(self):
        address_line1 = self.cleaned_data['address_line1']
        if Address.objects.filter(address_line1=address_line1).exists():
            raise forms.ValidationError("address already in use, please use another address")
        return address_line1

    def clean_address_line2(self):
        address_line2 = self.cleaned_data['address_line2']
        if Address.objects.filter(address_line2=address_line2).exists():
            raise forms.ValidationError("address already in use, please use another address")
        return address_line2

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise forms.ValidationError("phone can contain only digits")
        return phone

    def clean_postcode(self):
        postcode = self.cleaned_data['post_code']
        if not postcode.isdigit():
            raise forms.ValidationError("postcode can contain only digits")
        return postcode
