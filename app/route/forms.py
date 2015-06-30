# -*- coding: utf-8 -*-
from django import forms

from app.account.models import Account


class ChangeTextAuthorForm(forms.Form):
    # TODO написать отдельные mixin-ы или helper-ы для добавления одинаковых полей
    # TODO в queryset отображать лишь копирайтеров и редакторов
    text_author = forms.ModelChoiceField(queryset=Account.objects.all())

    def __init__(self, *args, **kwargs):
        self.step = kwargs.pop('step', None)
        self.action_name = kwargs.pop('action_name', None)
        self.request = kwargs.pop('request', None)
        super(ChangeTextAuthorForm, self).__init__(*args, **kwargs)

    def clean(self):
        # TODO вынести все, касаемое этого действия в родительское приложение Route,
        # чтобы можно было использовать в других маршрутах.
        # НО !!!!!!! запуск действия при сабмите должно быть переопределяемым
        self.cleaned_values = super(ChangeTextAuthorForm, self).clean()
        self.step.run_action(self.action_name, {'text_author': self.cleaned_values.get('text_author')})
        return self.cleaned_values
