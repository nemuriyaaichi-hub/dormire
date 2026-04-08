from uuid import uuid4

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        user = self.model(self, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "ユーザー"
        verbose_name_plural = "ユーザー"
        ordering = ("-created_at",)

    id = models.UUIDField(
        "uuid",
        default=uuid4,
        primary_key=True,
        editable=False,
    )
    username = models.CharField(
        "氏名",
        max_length=128,
    )

    email = models.EmailField(
        "メールアドレス",
        unique=True,
    )
    is_active = models.BooleanField(
        "アカウント有効性",
        default=True,
    )
    is_staff = models.BooleanField(
        "スタッフ権限",
        default=False,
    )
    is_crowd_funding_user = models.BooleanField(
        "クラウドファンディングユーザー権限",
        default=False,
    )
    is_furusato_tax_user = models.BooleanField(
        "ふるさと納税ユーザ権限",
        default=False,
    )
    is_salon_user = models.BooleanField(
        "サロンユーザ権限",
        default=False,
    )
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    objects = UserManager()

    @property
    def type(self):
        if self.is_superuser:
            return "admin"
        elif self.is_salon_user:
            return "salon"
        elif self.is_furusato_tax_user:
            return "furusato_tax"
        elif self.is_crowd_funding_user:
            return "crowd_funding"
