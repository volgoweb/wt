# -*- coding: utf-8 -*-
from django import forms
from ckeditor.widgets import CKEditorWidget

from helper.forms import BootstrapFormMixin
from .models import WikiPage

class WikiListFilters(forms.Form):
    pass


class WikiPageForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = WikiPage
        fields = '__all__'
        widgets = {
            'text': CKEditorWidget,
        }

    def __init__(self, *args, **kwargs):
        super(WikiPageForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'autofocus': '',
            # 'tabindex': 1,
        })
        # self.fields['text'].widget.attrs.update({
        #     'tabindex': 2,
        # })
        # self.fields['parent'].widget.attrs.update({
        #     'tabindex': 3,
        # })
