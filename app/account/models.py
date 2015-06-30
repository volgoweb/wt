# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    User,
    UserManager,
    PermissionsMixin,
)
from django.utils.translation import ugettext as _
from django.utils import timezone

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
    is_active = models.BooleanField(default=True)
    # должность
    job = models.CharField(_('job'), max_length = 50, null=True, blank=True)
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
