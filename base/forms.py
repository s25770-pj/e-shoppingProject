from django import forms
from django.forms import ModelForm
from .models import Product, Settings


class ProductForm(ModelForm):
    image = forms.ImageField(required=True)
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['host']


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        exclude = ['user']

    language = forms.ChoiceField(choices=Settings.LANGUAGE_CHOICES)
    theme = forms.ChoiceField(choices=Settings.THEME_CHOICES)
