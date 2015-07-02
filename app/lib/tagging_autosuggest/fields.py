#coding: utf-8
from __future__ import unicode_literals, absolute_import

from tagging.fields import TagField


class TagAutosuggestField(TagField):
    pass

try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    rules = [
        (
            (TagAutosuggestField, ),
            [],
            {
                "blank": ["blank", {"default": True}],
                "max_length": ["max_length", {"default": 255}],
                "max_tags": ["max_tags", {"default": False}],
            },
        ),
    ]
    add_introspection_rules(rules, ["^tagging_autosuggest\.fields",])