# -*- coding: utf-8 -*-

def accounts_list_to_choices(accounts):
    return [(u.pk, u) for u in accounts]
