# -*- coding: utf-8 -*-
from collections import OrderedDict
from django.db import models
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    User,
    UserManager,
    PermissionsMixin,
)
from django.utils.translation import ugettext as _
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

"""
# TODO Написать защиту от присвоении двух активных сотрудников на одну должность
"""


class CompanyUnitQueryset(models.query.QuerySet):
    def active(self, *args, **kwargs):
        return self.filter(active=True)

    def employee(self, *args, **kwargs):
        return self.filter(unit_type=self.model.UNIT_TYPE_EMPLOYEE)


class CompanyUnitManager(TreeManager):
    def get_queryset(self, *args, **kwargs):
        return CompanyUnitQueryset(self.model)

    def get_tree(self, node=None, filtered_ids=[]):
        """
        node - головной объект, от которого строим дерево,
        если он не указан, то строим дерево из всех объектов.
        """
        def get_descendants(node):
            descendents = []
            children = node.get_children()
            children.filter(pk__in=filtered_ids)
            for n in children:
                n_descendents = get_descendants(n)
                n_descendents = [n for n in n_descendents if n.pk in filtered_ids]
                descendents += n_descendents
            return [node] + descendents

        if node:
            tree = get_descendants(node)
        else:
            tree = []
            lev1_pages = self.filter(level=1)
            if filtered_ids:
                lev1_pages = self.filter(pk__in=filtered_ids)
            for node in lev1_pages:
                tree += get_descendants(node)
        from  more_itertools import unique_everseen
        tree = list(unique_everseen(tree))
        return tree


class CompanyUnit(MPTTModel):
    UNIT_TYPE_DEPARTMENT = 'dep'
    UNIT_TYPE_EMPLOYEE = 'emp'
    UNIT_TYPE_CHOICES = OrderedDict([
        (UNIT_TYPE_DEPARTMENT, u'Отдел'),
        (UNIT_TYPE_EMPLOYEE, u'Сотрудник'),
    ])

    name = models.CharField(max_length=200, verbose_name=u'Название')
    desc = models.TextField(verbose_name=u'Описание', blank=True, null=True)
    # TODO вынести пустой пункт choices в константы
    unit_type = models.CharField(max_length=15, choices=[('', '---------')]+UNIT_TYPE_CHOICES.items(), verbose_name=u'Тип')
    active = models.BooleanField(default=True, verbose_name=u'Активен')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    objects = CompanyUnitManager()

    class Meta:
        verbose_name = u'Элемент организационной структуры'
        verbose_name_plural = u'Элементы организационной структуры'

    def __unicode__(self, *args, **kwargs):
        return u'{name} ({unit_type}) №{pk}'.format(name=self.name, unit_type=self.unit_type, pk=self.pk)

    def get_absolute_url(self, *args, **kwargs):
        return reverse_lazy('account:company_unit_detail_page', kwargs={'pk': self.pk})

    def get_user(self):
        users = Account.objects.filter(
            is_active=True,
            job=self,
        )
        if users.count() > 1:
            # TODO обработать этот момент 
            assert False
        elif users.count() == 1:
            return users[0]
        return None


class AccountManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(
            email = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email,
            password = password,
        )
        user.is_superuser = True
        user.save(using = self._db)
        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)


class Account(AbstractBaseUser, PermissionsMixin):
    """
    Основной класс пользователя взамен django.contrib.auth.User
    """
    email = models.EmailField(_('email address'), max_length = 255, unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    middle_name = models.CharField(_('middle name'), max_length=30, null=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=30)
    # Флаг, для временного отключения учетки
    is_active = models.BooleanField(default=True, verbose_name=u'Активен')
    # должность
    # job = models.CharField(_('job'), max_length = 50, null=True, blank=True)
    job = models.ForeignKey('account.CompanyUnit', related_name='account', verbose_name=u'Должность', null=True, blank=True)
    # дата создания учетки
    created = models.DateTimeField(_('created'), default=timezone.now)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['password', 'first_name', 'last_name', 'job',]

    class Meta:
        verbose_name = u'Сотрудник'
        verbose_name_plural = u'Сотрудники'

    def get_full_name(self):
        return self.__str__()

    def get_short_name(self):
        return self.get_short_fio()

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return self.get_full_fio()

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def username(self):
        return self.email

    def get_username(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     print 'has_perm()'
    #     print perm
    #     print obj
    #     return True

    # def has_module_perms(self, app_label):
    #     # Active superusers have all permissions.
    #     if self.is_superuser:
    #         return True
    #     return _user_has_module_perms(self, app_label)

    def get_full_fio(self):
        if self.first_name and self.last_name:
            return u'{0} {1} {2}'.format(self.last_name, self.first_name, self.middle_name or '')
        else:
            return self.email

    def get_short_fio(self):
        short_first_name = ''
        if self.first_name:
            if self.middle_name:
                short_first_name = u'{0}.{1}.'.format(self.first_name[:1], self.middle_name[:1])
            else:
                short_first_name = u'{0}.'.format(self.first_name[:1])
        if self.last_name:
            return u'{0} {1}'.format(self.last_name, short_first_name)
        else:
            return self.email

    def save(self, *args, **kwargs):
        return super(Account, self).save(*args, **kwargs)

    # TODO добавить метод для того, чтобы в фикстурах можно было по мылу указывать пользователей
