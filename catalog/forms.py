from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Product, Version

exclusion_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'description':
                field.widget.attrs['class'] = 'uk-textarea'
                field.widget.attrs['style'] = 'height: 150px;'
            elif isinstance(self.fields[field_name], forms.CharField) or isinstance(self.fields[field_name],
                                                                                    forms.IntegerField):
                field.widget.attrs['class'] = 'uk-input'
            if isinstance(self.fields[field_name], forms.ModelChoiceField):
                field.widget.attrs['class'] = 'uk-select'
            if isinstance(self.fields[field_name], forms.BooleanField):
                field.widget.attrs['class'] = 'uk-checkbox'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price',)

    def clean_name(self):
        cleaned_name = self.cleaned_data['name']
        for exclusion_word in exclusion_words:
            if cleaned_name.find(exclusion_word) >= 0:
                raise forms.ValidationError('Не могут загружать запрещенные продукты на платформу.')
        return cleaned_name

    def clean_description(self):
        cleaned_description = self.cleaned_data['description']
        for exclusion_word in exclusion_words:
            if cleaned_description.find(exclusion_word) >= 0:
                raise forms.ValidationError('Не могут загружать запрещенные продукты на платформу.')
        return cleaned_description


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
