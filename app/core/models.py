# Import the abstract base user, base user manager, permissions mixin
"""to extend the Django user model whilst making use of some features that
come with the django model out of the box. backslash is used to break a
new line"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


# Create the manager class which is a class that provides the helper
# functions for creating a user or creating a super user.
class UserManager(BaseUserManager):

    """Extend the base user manager by pulling in all of the features that
    come with the base user manager and overriding a few functions to handle
    our email address instead of the username that expects"""
    def create_user(self, email, password=None, **extra_fields):
        """password=None: in case you want to create a user that is not active
        that doesn't have a password;
        **extra_fields: take any of the extra functions that are passed in
        when you call the create user function & pass them into the extra
        fields so that we can just add any additional fields that we create
        w/o user model, i.e., more flexibility to add new fields to our user,
        we don't have to add them here, we can just add them ad hoc as we add
        them to our mode.
        Creates and saves a new user - Description to our function"""
        if not email:
            raise ValueError('Users must have an email address')
        """Creating user with no email raises error"""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        """It's going to pass the email 1st and then anything extra that
        we add. The management commands allow you to access the model that
        the manager is for by typing self.model, this is effectively the
        same as creating a new user model and assigning it to the user
        variable"""
        user.set_password(password)
        """Password cannot be set in the previous call bcoz it needs to be
        encrypted. Use the set_password helper function that comes with the
        Django base user or the abstract base user"""
        user.save(using=self._db)
        """save the user, self._db is requird to support multiple database"""

        return user

    def create_superuser(self, email, password):
        """Create and save a new superuser
        we only create superuser with the command line, do not need to
        worry about the extra fields"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# Create the model
"""Extend the AbstractBaseUser and PermissionsMixin, this gives us all the
features that come out of the box with Django user model but we can then
build on top of them and customize it to support our email address"""


class User(AbstractBaseUser, PermissionsMixin):

    """Custom user model that suppots using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    """Define the fields of our database model, unique: 1 user w. 1 email.
    The models command here is the import added by defaut at the top.
    CharField is a standard character field.
    is_active is to determine if the user in the system is active or not
    so it allows us to deactive users that we require.
    is_staff to ensure the users are active but not staff - need a special
    command to create staff user
    is_superuser is included in PermissionsMixin, we don't include it here"""

    objects = UserManager()
    """Assign user manager to the object attribute, including the bracket
    at the end will create a new user manager for our object"""

    USERNAME_FIELD = 'email'
    """By default, the user name field is username and we're customising
    that to email so we cna use email address to log in"""
