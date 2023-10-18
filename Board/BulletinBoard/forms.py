from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import *


class AdForm(forms.ModelForm):
    text = forms.CharField(label='Контент', widget=CKEditorUploadingWidget())
    class Meta:
        model = Ad
        fields = ['title', 'type', 'text']

class ResponseForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

class AcceptResponseForm(forms.Form):
    accept = forms.BooleanField(initial=True, widget=forms.HiddenInput())

class RejectResponseForm(forms.Form):
    reject = forms.BooleanField(initial=False, widget=forms.HiddenInput())

class ResponseFilterForm(forms.Form):
    ad = forms.ModelChoiceField(
        queryset=Ad.objects.all(),
        empty_label="Все объявления",
        required=False
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ad'].queryset = Ad.objects.filter(author=user)


class MailingForm(forms.Form):
    text = forms.CharField(
        label='Текст для рассылки',
        widget=forms.Textarea(attrs={'rows': 7, 'cols': 60})
    )








