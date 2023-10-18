from django import forms
from django.contrib import admin
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class AdAdminForm(forms.ModelForm):
    text = forms.CharField(label = 'Контент', widget=CKEditorUploadingWidget())

    class Meta:
        model = Ad
        fields = '__all__'


class AdAdmin(admin.ModelAdmin):
    form = AdAdminForm


admin.site.register(Ad, AdAdmin)
admin.site.register(Response)
