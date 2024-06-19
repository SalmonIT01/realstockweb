from django import forms
from django.forms import ModelForm
from .models import Details

class VenueFrom(ModelForm):
    class Meta:
        model = Details
        fields = ('product_id','product_name','unit','amount','status_id')
        labels = {
            'product_id':'',
            'product_name':'',
            'unit':'',
            'amount':'',
            'status_id':'',
        }   
        # widgets = {
        #     'product_id' : forms.NumberInput(attrs={'class' : 'from-control'}), 
        #     'product_name' : forms.TextInput(attrs={'class' : 'from-control'}),
        #     'unit' : forms.TextInput(attrs={'class' : 'from-control'}),
        #     'amount' : forms.NumberInput(attrs={'class' : 'from-control'}),
        #     'status_id' : forms.NumberInput(attrs={'class' : 'from-control'})
        # }