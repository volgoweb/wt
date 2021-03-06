from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm, UserCreationForm

from .models import Account, CompanyUnit

class AccountCreationForm(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    class Meta:
        model = Account
        # fields = ('email',)
        exclude = []

    # def __init__(self, *args, **kwargs):
    #     super(AccountCreationForm, self).__init__(*args, **kwargs)
        # del(self.fields['username'])


class AccountChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    class Meta:
        model = Account
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super(AccountChangeForm, self).__init__(*args, **kwargs)
    #     del(self.fields['username'])


class AccountAdmin(UserAdmin):
    # The forms to add and change user instances
    form = AccountChangeForm
    add_form = AccountCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'last_name', 'first_name', 'email', 'department', 'job', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal info', {'fields': ('first_name', 'middle_name', 'last_name', 'department', 'job', 'time_zone')}),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(Account, AccountAdmin)


class CompanyUnitAdmin(admin.ModelAdmin):
    # The forms to add and change user instances
    list_display = ('id', 'name', 'parent', 'active')
    list_filter = ('parent', 'active')
    search_fields = ('name',)
    ordering = ('parent', 'name',)
    filter_horizontal = ()


admin.site.register(CompanyUnit, CompanyUnitAdmin)
