from django import forms
from .models import post
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

class Postform(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('POST', 'POST', css_class= 'btn-primary'))

    class Meta:
        model = post
        fields = [
            'image',
            'caption'
        ]