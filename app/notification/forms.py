# -*- coding: utf-8 -*-
from django import forms

from helper.forms import BootstrapFormMixin

class NotificationsListFilters(BootstrapFormMixin, forms.Form):
    readed = forms.ChoiceField(
        choices=[
            ('', u'Все'),
            ('unreaded', u'Только непрочитанные'),
        ],
        label=u'Прочитано',
        required=False,
        widget=forms.RadioSelect(),
    )
