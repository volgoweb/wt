# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse_lazy
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, m2m_changed

from .signals import wiki_page_saved
from app.account.models import CompanyUnit, Account


class WikiPageQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(deleted=False)

    def can_edit(self, user):
        # TODO сделать правильно
        return self.filter(editors=user.job)


class WikiPageManager(TreeManager):
    def get_queryset(self):
        return WikiPageQueryset(self.model)#.active()

    def get_tree(self, node=None, perm=None, user=None):
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
            for n in children:
                descendents += get_descendants(n)
            return [node] + descendents

        if node:
            tree = get_descendants(node)
        else:
            tree = []
            lev0_pages = self.filter(level=0)
            for node in lev0_pages:
                tree += get_descendants(node)
        if perm:
            # TODO кэшировать список пользователей и по ним фильтровать
            tree = filter(lambda node: node.has_user_perm_in_wiki_page(perm=perm, user=user), tree)

        return tree


class WikiPage(MPTTModel):
    PERM_VIEW = 'view'
    PERM_EDIT = 'edit'

    title = models.CharField(max_length=255, verbose_name=u'Заголовок', db_index=True)
    text = models.TextField(max_length=50000, verbose_name=u'Текст')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'Родительская глава', db_index=True)
    performers = models.ManyToManyField(
        'account.CompanyUnit',
        related_name='wiki_performer',
        verbose_name=u'Исполнители',
        help_text=u'Отделы или должности, для кого предназначена данная глава.',
    )
    subscribers = models.ManyToManyField(
        'account.CompanyUnit',
        related_name='wiki_subscriber',
        verbose_name=u'Читатели главы',
        help_text=u'Отделы или должности, кто может читать главу и получать уведомления о ее изменении.',
    )
    editors = models.ManyToManyField(
        'account.CompanyUnit',
        related_name='wiki_editor',
        verbose_name=u'Авторы главы',
        help_text=u'Отделы или должности, кто может редактировать главу и добавлять вложенные главы.',
    )
    deleted = models.BooleanField(default=False, verbose_name=u'Удаленная')

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

    def is_company_unit_field_contains_user(self, field_name, user):
        # field = getattr(self, field_name)
        # if not user.job:
        #     return False
        # user_dep_pk = getattr(user.job.parent, 'pk', None)
        # if field.filter(unit_type=CompanyUnit.UNIT_TYPE_EMPLOYEE, pk=user.job.pk):
        #     return True
        # deps = field.filter(unit_type=CompanyUnit.UNIT_TYPE_DEPARTMENT)
        # # проходим по всем отделам, указанным в поле 
        # for dep in deps:
        #     # проверяем входит ли указанный сотрудник в какой-то отдел или подчиненный подотдел
        #     descendants = dep.get_descendants(include_self=True)
        #     descendant_ids = [d.pk for d in descendants]
        #     if user_dep_pk in descendant_ids:
        #         return True

        # users = self.get_users_of_company_unit_field(field_name)
        # if user in users:
        #     return True

        # TODO написать queryset метод для этого
        extra = WikiPageExtra.objects.get(wiki_page=self)
        if user in getattr(extra, '%s_users' % field_name).all():
            return True
        return False

    def has_user_perm_in_wiki_page(self, user, perm):
        if user.is_superuser:
            return True
        if perm == self.PERM_VIEW:
            if self.is_company_unit_field_contains_user(field_name='performers', user=user) \
            or self.is_company_unit_field_contains_user(field_name='subscribers', user=user):
                return True
        elif perm == self.PERM_EDIT:
            return self.has_user_perm_edit_in_wiki_page(user)
        return False

    def has_user_perm_edit_in_wiki_page(self, user):
        if self.is_company_unit_field_contains_user(field_name='editors', user=user):
            return True
        else:
            return False

    def get_users_of_company_unit_field(self, field_name):
        field = getattr(self, field_name)
        all_units = []
        for unit in field.all():
            all_units += [unit]
            if unit.unit_type == CompanyUnit.UNIT_TYPE_DEPARTMENT:
                # для случаев, когда выбран отдел, а в отделе по иеррархии сначала идет начальник отдела,
                # а ему (вглубь по дереву) подчиняются подчиненные выбираем всех подчиненных
                def get_children_if_one_employee(children):
                    if len(children) == 1:
                        if children[0].unit_type == CompanyUnit.UNIT_TYPE_EMPLOYEE:
                            sub_children = list(children[0].get_children())
                            children += get_children_if_one_employee(sub_children)
                    return children

                children = get_children_if_one_employee(list(unit.get_children()))
                children = filter(lambda u: u.unit_type == CompanyUnit.UNIT_TYPE_EMPLOYEE, children)
                all_units += children
        users = Account.objects.filter(job__in=all_units)
        # assert False
        return users


class WikiPageExtra(models.Model):
    wiki_page = models.ForeignKey('wiki.WikiPage', related_name='extra')
    performers_users = models.ManyToManyField('account.Account',
        related_name='wiki_performer_user',
        verbose_name=u'Исполнители',
        help_text=u'Сотрудники, для кого предназначена данная глава.'
    )
    subscribers_users = models.ManyToManyField('account.Account',
        related_name='wiki_subscriber_user',
        verbose_name=u'Читатели главы',
        help_text=u'Сотрудники, кто может читать главу и получать уведомления о ее изменении.',
    )
    editors_users = models.ManyToManyField('account.Account',
        related_name='wiki_editor_user',
        verbose_name=u'Авторы главы',
        help_text=u'Сотрудники, кто может редактировать главу и добавлять вложенные главы.',
    )

    def update_company_field_fields(self):
        for field_name in ['performers', 'subscribers', 'editors']:
            users = self.wiki_page.get_users_of_company_unit_field(field_name)
            extra_field_name = '%s_users' % field_name
            extra_field = getattr(self, extra_field_name, None)
            if extra_field:
                extra_field.clear()
                extra_field.add(*users)


@receiver(wiki_page_saved, sender=WikiPage)
def post_full_save_wiki_page(wiki_page, created, request, **kwargs):
    if created:
        ext = WikiPageExtra(
            wiki_page=wiki_page,
        )
        ext.save()
    else:
        ext = WikiPageExtra.objects.get(wiki_page=wiki_page)
    ext.update_company_field_fields()
    ext.save()


@receiver(post_save, sender=Account)
def post_save_account(**kwargs):
    # TODO перенести в ассинхронное выполнение через celery
    for ext in WikiPageExtra.objects.all():
        ext.update_company_field_fields()
        ext.save()

@receiver(post_save, sender=CompanyUnit)
def post_save_company_unit(**kwargs):
    # TODO перенести в ассинхронное выполнение через celery
    for ext in WikiPageExtra.objects.all():
        ext.update_company_field_fields()
        ext.save()
