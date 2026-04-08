import os
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

User = get_user_model()


def get_image_path(self, filename):
    prefix = "vp-images/"
    name = str(uuid4())
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension


class Measure(models.Model):
    class Meta:
        verbose_name = "VP計測結果（オーダー用）"
        verbose_name_plural = "VP計測結果（オーダー用）"
        ordering = ("-created_at",)

    id = models.UUIDField(
        "uuid",
        default=uuid4,
        primary_key=True,
        editable=False,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    right_arm_length = models.FloatField("右腕の長さ")
    left_arm_length = models.FloatField("左腕の長さ")
    right_leg_length = models.FloatField("右足の長さ")
    left_leg_length = models.FloatField("左足の長さ")
    knee_ankle = models.FloatField("膝から足首までの長さ")
    back_length = models.FloatField("背中の長さ")
    back_angle = models.FloatField("背中の角度")
    head_angle = models.FloatField("頭の傾き")
    shoulder_angle = models.FloatField("肩の角度")
    hip_angle = models.FloatField("骨盤の角度")
    neck_base = models.FloatField("首の付け根")
    neck_width = models.FloatField("首（首の凹みと付け根の幅）")
    head_width = models.FloatField("頭（後頭部と付け根の幅）")
    posture = models.CharField("姿勢診断", max_length=1)
    # サポートパッド用
    neck_hip = models.FloatField("首から骨盤中央までの長さ")
    hip_knee = models.FloatField("骨盤中央から膝までの長さ")
    # 枕用
    right_shoulder_width = models.FloatField("右半身の肩幅")
    left_shoulder_width = models.FloatField("左半身の肩幅")
    right_ear_shoulder = models.FloatField("右半身の耳から肩までの長さ")
    left_ear_shoulder = models.FloatField("左半身の耳から肩までの長さ")
    # images
    image1 = models.ImageField(
        "画像1",
        upload_to=get_image_path,
        null=True,
        blank=True,
    )
    image2 = models.ImageField(
        "画像2",
        upload_to=get_image_path,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)


class MeasureOnly(models.Model):
    class Meta:
        verbose_name = "VP計測結果（整体師モード）"
        verbose_name_plural = "VP計測結果（整体師モード）"
        ordering = ("-created_at",)

    id = models.UUIDField(
        "uuid",
        default=uuid4,
        primary_key=True,
        editable=False,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(
        "名前（漢字）",
        max_length=128,
        null=True,
    )
    kana = models.CharField(
        "名前（カナ）",
        max_length=128,
        null=True,
    )
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone_number = models.CharField(
        "電話番号",
        max_length=16,
        validators=[phoneNumberRegex],
        blank=True,
        null=True,
    )
    email = models.EmailField(
        "メールアドレス",
        blank=True,
        null=True,
    )
    post_code = models.CharField(
        "郵便番号",
        max_length=8,
        blank=True,
        null=True,
    )
    address = models.TextField(
        "住所",
        blank=True,
        null=True,
    )
    building = models.TextField(
        "建物名",
        blank=True,
        null=True,
    )
    right_arm_length = models.FloatField("右腕の長さ")
    left_arm_length = models.FloatField("左腕の長さ")
    right_leg_length = models.FloatField("右足の長さ")
    left_leg_length = models.FloatField("左足の長さ")
    knee_ankle = models.FloatField("膝から足首までの長さ")
    back_length = models.FloatField("背中の長さ")
    back_angle = models.FloatField("背中の角度")
    head_angle = models.FloatField("頭の傾き")
    shoulder_angle = models.FloatField("肩の角度")
    hip_angle = models.FloatField("骨盤の角度")
    neck_base = models.FloatField("首の付け根")
    neck_width = models.FloatField("首（首の凹みと付け根の幅）")
    head_width = models.FloatField("頭（後頭部と付け根の幅）")
    posture = models.CharField("姿勢診断", max_length=1)
    # サポートパッド用
    neck_hip = models.FloatField("首から骨盤中央までの長さ")
    hip_knee = models.FloatField("骨盤中央から膝までの長さ")
    # 枕用
    right_shoulder_width = models.FloatField("右半身の肩幅")
    left_shoulder_width = models.FloatField("左半身の肩幅")
    right_ear_shoulder = models.FloatField("右半身の耳から肩までの長さ")
    left_ear_shoulder = models.FloatField("左半身の耳から肩までの長さ")
    # images
    image1 = models.ImageField(
        "画像1",
        upload_to=get_image_path,
        null=True,
        blank=True,
    )
    image2 = models.ImageField(
        "画像2",
        upload_to=get_image_path,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)
