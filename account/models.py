from datetime import datetime
from unicodedata import category
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
    AbstractUser,
)
from django.contrib import auth
from django.utils.translation import gettext_lazy as _
import uuid
from django.utils import timezone


# The UserAccountManager class is a custom manager class that overrides the default manager class.
# This class is used to override the default manager class and add custom functionality to it.
class UserAccountManager(BaseUserManager):
    def _create_user(self, email, first_name, last_name, password, **extra_fields):
        """
        Create a new user object with the given email, first_name, last_name, and password.

        :param email: The email address of the user
        :param first_name: The first name of the user
        :param last_name: The last_name of the user
        :param password: The password for the user
        :return: A user object.
        """

        if not email:
            raise ValueError("User must have an email address")
        email = self.normalize_email(email).lower()
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, email, first_name=None, last_name=None, password=None, **extra_fields
    ):
        """
        Create a new user object.

        :param email: The email address of the user
        :param first_name: The first name of the user
        :param last_name: The last_name of the user
        :param password: The password for the new user
        :return: A User object.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        return self._create_user(email, first_name, last_name, password, **extra_fields)

    def create_saff(
        self, email, first_name=None, last_name=None, password=None, **extra_fields
    ):
        """
        Create a new user, with the given email, first name, last_name, and password.
        The function also sets is_staff and is_superuser to True and False respectively.
        If is_staff or is_superuser aren't included in the extra_fields dictionary, they are set to True and
        False respectively.
        If is_staff is set to True, is_superuser is automatically set to False.
        If is_superuser is set to True, is_staff is automatically set to True.

        :param email: The email address of the user
        :param first_name: The first name of the user
        :param last_name: The last_name of the user
        :param password: The password for the new user
        :return: A User object.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Staff must have is_staff = True")
        if extra_fields.get("is_superuser") is True:
            raise ValueError("Staff cannot have is_staff = True")

        return self._create_user(email, first_name, last_name, password, **extra_fields)

    def create_superuser(
        self, email, first_name=None, last_name=None, password=None, **extra_fields
    ):
        """
        Create a new user with the given email, first name, last_name, and password.
        Then, create a superuser with the given email, first name, last_name, and password.
        The superuser is given the default permissions of a superuser.
        The function returns the newly created user.

        :param email: The email address of the user
        :param first_name: The first name of the user
        :param last_name: last_name of the user
        :param password: The password for the new user
        :return: A User object.
        """
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff = True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self._create_user(email, first_name, last_name, password, **extra_fields)



# The User class is a custom user model that inherits from the AbstractBaseUser class and the
# PermissionsMixin class. This class is used to add custom functionality to the default user model.
# The UserAccountManager class is a custom manager class that overrides the default manager class.
# This class is used to override the default manager class and add custom functionality to it.
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), blank=True, unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
   
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    registration_complete = models.BooleanField(
        _("registration complete"),
        default=False,
        help_text=_(
            "Designates whether this user has completed the registration process."
            "use this to determine if the user should be allowed to access the rest of the site."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    
   

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserAccountManager()

    def __str__(self):
        return str(self.email)

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_first_name(self):
        return str(self.first_name)

    def get_last_name(self):
        return str(self.last_name)

    def get_country(self):
        return str(self.country.name)

    def get_country_flag(self):
        return str(self.country.flag)
