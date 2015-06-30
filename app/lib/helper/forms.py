# -*- coding: utf-8 -*-
from django import forms


class BootstrapFormMixin(object):
    def __init__(self, *args, **kwargs):
        super(BootstrapFormMixin, self).__init__(*args, **kwargs)
        self.add_widget_attrs()

    def add_widget_attrs(self):
        for f in self.fields.values():
            f.widget.attrs['class'] = f.widget.attrs.get('attrs', '') + ' form-control'


class URLPlaceholderMixin(object):
    """
    Добавляет placeholder для полей типа URLField.
    """
    def __init__(self, *args, **kwargs):
        super(URLPlaceholderMixin, self).__init__(*args, **kwargs)
        self.add_placeholders_to_url_fields()

    def add_placeholders_to_url_fields(self, *args, **kwargs):
        for f in self.fields.values():
            if isinstance(f, forms.URLField):
                f.widget.attrs.update({'placeholder': 'http://'})
