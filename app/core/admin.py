from core import models

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
"""Need to import the default Django user admin, need to change some
of the class variables to support our custom user admin using email
instead of username"""
from django.utils.translation import gettext as _
"""Import gettext function to convert strings in python to human
readable text, in this context, the strings get passed through the
transalation engine so we're not doing anything with translation.
If you want to extend the code to support multiple languages then this
would make easier for you to do that bcoz you just set up the transalation
files and then it'll convert the text appropriately"""


class UserAdmin(BaseUserAdmin):
    """"Create our custom user admin by extending the BaseUserAdmin"""
    ordering = ['id']
    list_display = ['email', 'name']
    """Define the field set for test 2, each bracket is a section,
    1st section: no title, contains 2 fields email, pw
    2nd section: title: personal info, contains 1 field, needs to
    add a comma after the only field otherwise it'll be recognised as
    a string and won't work
    3rd section: permission, contains 3 fields
    4th section: Important dates, contains 1 field"""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    """Define the additional field set for test 3 to include email,
    password, password 2 to create a new user. The user admin by
    default takes an add field sets which defines the fields that you
    include on the add page which is the same as the create user page,
    remember to add the comma at the end of the first item as it's the
    only item, w/o the comma, python will be confused it as a string.
    Classes assigned to the form: default option"""
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
                }),
    )


admin.site.register(models.User, UserAdmin)
"""Register the site in the Django admin"""
