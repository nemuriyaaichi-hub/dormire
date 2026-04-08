from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models

from recommends.models import Hearing, MatRec, PillowRec

User = get_user_model()


class Customer(models.Model):
    class Meta:
        verbose_name = "注文顧客情報"
        verbose_name_plural = "注文顧客情報"
        ordering = ("-created_at",)

    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    id = models.UUIDField(
        "uuid",
        default=uuid4,
        primary_key=True,
        editable=False,
    )
    name = models.CharField("顧客名", max_length=128)
    kana = models.CharField("フリガナ", max_length=128)
    phone_number = models.CharField(
        "電話番号",
        max_length=16,
        validators=[phoneNumberRegex],
    )
    email = models.EmailField("メールアドレス")
    post_code = models.CharField("郵便番号", max_length=8)
    address = models.TextField("住所")
    building = models.TextField(
        "建物名",
        null=True,
    )
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)


class PillowOrder(models.Model):
    class Meta:
        verbose_name = "枕オーダー情報"
        verbose_name_plural = "枕オーダー情報"
        ordering = ("-created_at",)

    id = models.UUIDField(
        "uuid",
        default=uuid4,
        primary_key=True,
        editable=False,
    )
    pillow_rec = models.ForeignKey(
        PillowRec,
        verbose_name="枕レコメンド",
        on_delete=models.CASCADE,
    )
    material = models.CharField("枕素材", max_length=10)
    cover_material = models.CharField("カバー素材", max_length=10, null=True)
    cover_color1 = models.IntegerField(
        "カバー色１",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
        null=True,
    )
    cover_color2 = models.IntegerField(
        "カバー色２",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
        null=True,
    )
    cover_color3 = models.IntegerField(
        "カバー色３",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
        null=True,
    )
    created_at = models.DateTimeField("作成日時", auto_now_add=True)

    @property
    def cover_count(self):
        gray = self.cover_color1 if self.cover_color1 else 0
        beige = self.cover_color2 if self.cover_color2 else 0
        pink = self.cover_color3 if self.cover_color3 else 0
        return gray + beige + pink


class MatOrder(models.Model):
    class Meta:
        verbose_name = "マットレスオーダー情報"
        verbose_name_plural = "マットレスオーダー情報"
        ordering = ("-created_at",)

    id = models.UUIDField(
        "uuid",
        default=uuid4,
        primary_key=True,
        editable=False,
    )
    mat_rec1 = models.ForeignKey(
        MatRec,
        verbose_name="マットレスレコメンド1",
        on_delete=models.CASCADE,
        related_name="mat_rec1",
    )
    mat_rec2 = models.ForeignKey(
        MatRec,
        verbose_name="マットレスレコメンド2",
        on_delete=models.CASCADE,
        related_name="mat_rec2",
        null=True,
    )
    size = models.CharField("サイズ", max_length=10)
    thickness = models.IntegerField("厚み")
    cover_material = models.CharField("カバー素材", max_length=10, null=True)
    cover_color1 = models.IntegerField(
        "カバー色１",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
        null=True,
    )
    cover_color2 = models.IntegerField(
        "カバー色２",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
        null=True,
    )
    cover_color3 = models.IntegerField(
        "カバー色３",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
        null=True,
    )
    created_at = models.DateTimeField("作成日時", auto_now_add=True)

    @property
    def cover_count(self):
        gray = self.cover_color1 if self.cover_color1 else 0
        beige = self.cover_color2 if self.cover_color2 else 0
        pink = self.cover_color3 if self.cover_color3 else 0
        return gray + beige + pink


class Order(models.Model):
    class Meta:
        verbose_name = "オーダー総合情報"
        verbose_name_plural = "オーダー総合情報"
        ordering = ("-created_at",)

    id = models.UUIDField(
        "注文ID",
        default=uuid4,
        primary_key=True,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        verbose_name="ユーザー",
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey(
        Customer,
        verbose_name="注文者",
        on_delete=models.CASCADE,
        related_name="customer",
    )
    pillow_order1 = models.OneToOneField(
        PillowOrder,
        verbose_name="枕オーダー1",
        on_delete=models.CASCADE,
        related_name="pillow_order1",
        blank=True,
        null=True,
    )
    pillow_order2 = models.OneToOneField(
        PillowOrder,
        verbose_name="枕オーダー2",
        on_delete=models.CASCADE,
        related_name="pillow_order2",
        blank=True,
        null=True,
    )
    mat_order = models.OneToOneField(
        MatOrder,
        verbose_name="マットレスオーダー",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    hearing1 = models.ForeignKey(
        Hearing,
        verbose_name="ヒアリング1人目",
        on_delete=models.CASCADE,
        related_name="hearing1",
        blank=True,
        null=True,
    )
    hearing2 = models.ForeignKey(
        Hearing,
        verbose_name="ヒアリング2人目",
        on_delete=models.CASCADE,
        related_name="hearing2",
        blank=True,
        null=True,
    )
    memo = models.TextField("ねむりやメモ", null=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
