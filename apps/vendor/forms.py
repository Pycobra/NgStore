from django import forms
from django.forms import inlineformset_factory, modelformset_factory

from apps.product.models import Product, ProductSpecificationValue, ProductImages
from apps.vendor.models import Vendor



"""class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']"""

class ProductForm(forms.ModelForm):
    title = forms.CharField(min_length=2, max_length=100)
    in_stock = forms.BooleanField(label='In stock:')

    class Meta:
        model = Product
        fields = ['product_type', 'category', 'title', 'description', 'price', 'discount_price', 'in_stock',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_type'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Product Type'})
        self.fields['category'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Category'})
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Title'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Description', 'id':'textarea'})
        self.fields['price'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Price'})
        self.fields['discount_price'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Discount Price'})
        self.fields['in_stock'].widget.attrs.update({'id':'checkbox'})






class ProductSpecForm(forms.ModelForm):
    class Meta:
        model = ProductSpecificationValue
        fields = ['specification', 'value']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['specification'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Specification'})
        self.fields['value'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Value'})

class ProductImageForm(forms.ModelForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = ProductImages
        fields = ['images',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['images'].widget.attrs.update({'class': 'form-control'})

class ProductImageForm2(forms.ModelForm):
    listed = []
    num = 0
    #INITIAL_FORMS = forms.CharField(widget=forms.HiddenInput())
    #YES_OR_NO = ((True, 'Yes'),(False,'no'))
    #is_main = forms.BooleanField(widget=forms.RadioSelect(choices=YES_OR_NO), required=False)
    class Meta:
        model = ProductImages
        fields = ['images', 'is_main',]# 'TOTAL_FORMS', 'INITIAL_FORMS',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['images'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_main'].widget.attrs.update({'class':'checkbox', 'data-index':kwargs['prefix']})
        #self.fields['TOTAL_FORMS'].widget.attrs.update({'blank':'True'})
        #self.fields['INITIAL_FORMS'].widget.attrs.update({'blank':'True'})


    def clean_is_main(self):
        is_main = self.cleaned_data['is_main']
        self.listed.append(is_main)
        #print(is_main)
        #raise forms.ValidationError("This store name already taken")
        return is_main

class ProductForm2(forms.ModelForm):
    category = forms.CharField(label='Category', min_length=4,  max_length=50, help_text='Required', error_messages={'required':'Sorry, you will need an email'})
    title = forms.CharField(label='Title', min_length=4, max_length=100, help_text='Required', error_messages={'required':'Sorry, you will need an email'})
    Description = forms.CharField(label='Description', max_length=100, help_text='Required', error_messages={'required':'Sorry, you will need an email'})
    price = forms.IntegerField(label='Price', help_text='Required', error_messages={'required':'Sorry, you will need an email'})

class VendorEditForm(forms.ModelForm):
    store_name = forms.CharField(label='Store name', min_length=3, max_length=100,error_messages={'required':'Sorry, enter your new store name'},
                              widget=forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'Store name', 'id': 'login'
                                                                                                                        'edit-storename'}))

    vendor_image = forms.ImageField(label='Choose image')
    class Meta:
        model= Vendor
        fields=('store_name', "vendor_image")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vendor_image'].widget.attrs.update(
            {'class': 'image-control'})

class VendorRegistrationForm(forms.ModelForm):
    store_name = forms.CharField(label='Enter Store Name', min_length=4, max_length=255)
    class Meta:
        model= Vendor
        fields=('store_name', "vendor_image")

    def clean_store_name(self):
        store_name = self.cleaned_data['store_name'].lower()
        in_exists= Vendor.objects.filter(store_name=store_name)
        if in_exists.count():
            raise forms.ValidationError("This storeName already taken")
        return store_name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['store_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'StoreName', 'id': 'store_name'})
        self.fields['vendor_image'].widget.attrs.update(
            {'class': 'image-control'})