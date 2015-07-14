# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse_lazy
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager


class WikiPageManager(TreeManager):
    def get_tree(self, node=None, field_for_permission=None, user=None):
        """
        node - головной объект, от которого строим дерево,
        если он не указан, то строим дерево из всех объектов.

        filed_for_permission - поле (for_appointments, can_read_appointments, can_edit_appointments),
        определяющее список должностей, к которым относится данная страница wiki.
        Если это поле указана, то в дереве присутствуют лишь те объекты,
        у которых указанный пользователь (параметр user) имеет должность,
        указанную в данном поле.
        """
        def get_descendants(node):
            descendents = []
            children = node.get_children()
            if field_for_permission:
                children = filter_qs_by_perm(children)
            for n in children:
                descendents += get_descendants(n)
            return [node] + descendents

        def filter_qs_by_perm(qs):
            perm_kwargs = {
                field_for_permission: user.appointment,
            }
            return qs.filter(**perm_kwargs)


        if node:
            tree = get_descendants(node)
        else:
            tree = []
            lev1_pages = self.filter(level=1)
            if field_for_permission:
                lev1_pages = filter_qs_by_perm(lev1_pages)
            for node in lev1_pages:
                tree += get_descendants(node)
        return tree


class WikiPage(MPTTModel):
    title = models.CharField(max_length=255, verbose_name=u'Заголовок', db_index=True)
    text = models.TextField(max_length=50000, verbose_name=u'Текст')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'Родительская глава', db_index=True)

    objects = WikiPageManager()

    # class Meta:
    #     ordering = ['level', 'pk']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('wiki:wiki_page_detail', kwargs={'pk': self.pk,})

    def render_descendants(self):
        html = ''
        for node in self.get_children():
            html += u'<div>{0}</div>'.format(self.title)
            html += node.render_descendants()
        return html
