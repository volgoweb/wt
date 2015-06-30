# -*- coding: utf-8 -*-
from django import forms


class FormsetWidget(forms.widgets.Widget):
    """
    Виджет для вывода formset, вложенного в форму.
    Используется для поля FormsetField
    """
    def render(self, name, value, attrs=None):
        return self.attrs['formset']

