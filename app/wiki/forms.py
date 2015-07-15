# -*- coding: utf-8 -*-
from django import forms
from ckeditor.widgets import CKEditorWidget
from django.core.exceptions import ValidationError

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
        self.request = kwargs.pop('request', None)
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
        # self.fields['parent'].queryset = WikiPage.objects.all().active().can_edit(self.request.user)

    def clean_parent(self, *args, **kwargs):
        parent = self.cleaned_data['parent']
        if parent:
            if not parent.has_user_perm_in_wiki_page(user=self.request.user, perm=WikiPage.PERM_EDIT):
                raise ValidationError(u'Не разрешено добавлять страницы в главу "{0}"'.format(parent))
        return parent
