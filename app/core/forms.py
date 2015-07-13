# -*- coding: utf-8 -*-
from django import forms
from ajax_upload.widgets import AjaxClearableFileInput

from .models import FileItem

class FileItemForm(forms.ModelForm):
    class Meta:
        model = FileItem
        fields = '__all__'
        widgets = {
            'file': AjaxClearableFileInput,
        }
