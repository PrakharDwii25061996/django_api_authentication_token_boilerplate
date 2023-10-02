""" accounts.models.py """
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _


class MyAccountManager(BaseUserManager):
    """
    This is a manager for Account class 
    """
    def create_user(self, email, full_name=None, password=None, **kwargs):
        user  = self.model(
                email=self.normalize_email(email),
            )

        if not email:
            raise ValueError("Users must have an Emaill address")

        if full_name:
            user.full_name = full_name


        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
                email=self.normalize_email(email),
                password=password,
            )
        user.is_admin = True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    """
    Custom user class inheriting AbstractBaseUser class 
    """
    username = None
    email = models.EmailField(_('email address'), unique=True)
    full_name     = models.CharField(max_length=255, null=True)
    date_joined   = models.DateTimeField(verbose_name='date joined', auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
