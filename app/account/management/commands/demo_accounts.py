# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from smk.account.models import Account

class Command(BaseCommand):
    help = u'Создает демо-пользователей.'

    def handle(self, *args):
        call_command('loaddata', 'demo_accounts.yaml')

        # добавляем нужные права для некоторых пользователей
        spec = Account.objects.get(email='ir_specialist@smk.ru')
        # spec.permission
