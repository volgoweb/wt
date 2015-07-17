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

    # def __init__(self, *args, **kwargs):
    #     super(FileItemForm, self).__init__(*args, **kwargs)
    #     self.fields['file'].required = True

    # def clean_file(self):
    #     values = self.cleaned_data
    #     print '---------------- clean_file'
    #     print values
    #     if not values['file']:
    #         values['deleted'] = True
    #     return values['file']
