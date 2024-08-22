from django import forms

from .models import Tag
# let's assume we want to create Tags using a form


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'
