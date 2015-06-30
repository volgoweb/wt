# -*- coding: utf-8 -*-
from django import forms

from .widgets import FormsetWidget

class FormsetField(forms.Field):
    """
    Поле, выводящее formset.
    """
    def __init__(self, formset, *args, **kwargs):
        widget = FormsetWidget(attrs={
            'formset': formset,
        })
        kwargs.update({
            'widget': widget,
            'required': False
        })
        super(FormsetField, self).__init__(*args, **kwargs)
