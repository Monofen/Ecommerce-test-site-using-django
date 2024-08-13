# forms.py
from django import forms
from products.models import Product, ElectronicProduct

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'description', 'on_sale', 'sale_price']
    
    screen = forms.ChoiceField(choices=ElectronicProduct.SCREEN_CHOICES, required=False)
    ram = forms.ChoiceField(choices=ElectronicProduct.RAM_CHOICES, required=False)
    
    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        
        if product and product.category.is_electronics:
            electronic_features = ElectronicProduct.objects.filter(product=product).first()
            if electronic_features:
                self.fields['screen'].initial = electronic_features.screen
                self.fields['ram'].initial = electronic_features.ram
        else:
            # Hide the fields if not an electronic product
            self.fields.pop('screen', None)
            self.fields.pop('ram', None)

    def save(self, commit=True):
        product = super().save(commit=False)
        if product.category.is_electronics:
            electronic_features, created = ElectronicProduct.objects.get_or_create(product=product)
            electronic_features.screen = self.cleaned_data.get('screen')
            electronic_features.ram = self.cleaned_data.get('ram')
            if commit:
                product.save()
                electronic_features.save()
        else:
            if commit:
                product.save()
        return product
