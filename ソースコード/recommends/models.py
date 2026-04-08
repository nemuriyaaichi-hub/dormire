from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from measure.models import Measure

User = get_user_model()


class PillowBase(models.Model):
    class Meta:
        verbose_name = "枕ベースデータ"
        verbose_name_plural = "枕ベースデータ"

    id = models.UUIDField(
        "uuid",
        default=uuid4,
        primary_key=True,
        editable=False,
    )
    material = models.CharField("枕素材", max_length=15)
    position1 = models.IntegerField("位置１")
    position2 = models.IntegerField("位置２")
    position3 = models.IntegerField("位置３")
    position4 = models.IntegerField("位置４")
    position5 = models.IntegerField("位置５")
    position6 = models.IntegerField("位置６")
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)


class MatBase(models.Model):
    class Meta:
        verbose_name = "マットレスベースデータ"
        verbose_name_plural = "マットレスベースデータ"
        indexes = [
            models.Index(
                fields=[
                    "sex",
                    "have_backache",
                    "have_shoulder_pain",
                    "posture",
                    "hardness",
                    "bmi_min",
                    "bmi_max",
                    "height_min",
                    "height_max",
                ]
            ),
        ]

    id = models.UUIDField(
        "uuid",
        default=uuid4,
        primary_key=True,
        editable=False,
    )
    sex = models.IntegerField(
        "性別",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(2),
        ],
    )
    height_min = models.IntegerField("身長下限")
    height_max = models.IntegerField("身長上限")
    bmi_min = models.DecimalField("BMI下限", max_digits=3, decimal_places=1)
    bmi_max = models.DecimalField("BMI上限", max_digits=3, decimal_places=1)
    have_backache = models.BooleanField("腰痛")
    have_shoulder_pain = models.BooleanField("肩の痛み")
    hardness = models.IntegerField(
        "硬さ",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )
    posture = models.CharField("姿勢タイプ", max_length=1)
    position1 = models.CharField("位置１", max_length=10)
    position2 = models.CharField("位置２", max_length=10)
    position3 = models.CharField("位置３", max_length=10)
    position4 = models.CharField("位置４", max_length=10)
    position5 = models.CharField("位置５", max_length=10)
    position6 = models.CharField("位置６", max_length=10)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)


class PillowRec(models.Model):
    class Meta:
        verbose_name = "おすすめ枕"
        verbose_name_plural = "おすすめ枕"

    id = models.UUIDField(
        "uuid",
        default=uuid4,
        primary_key=True,
        editable=False,
    )
    sheet = models.IntegerField(
        "シートの厚み",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(4),
        ],
    )
    position1 = models.IntegerField("位置１")
    position2 = models.IntegerField("位置２")
    position3 = models.IntegerField("位置３")
    position4 = models.IntegerField("位置４")
    position5 = models.IntegerField("位置５")
    position6 = models.IntegerField("位置６")
    diff_position1 = models.IntegerField("差分位置１")
    diff_position2 = models.IntegerField("差分位置２")
    diff_position3 = models.IntegerField("差分位置３")
    diff_position4 = models.IntegerField("差分位置４")
    diff_position5 = models.IntegerField("差分位置５")
    diff_position6 = models.IntegerField("差分位置６")
    created_at = models.DateTimeField("作成日時", auto_now_add=True)

    @property
    def con_sheet(self):
        if self.sheet == 1:
            sheet = "小"
        elif self.sheet == 2:
            sheet = "大"
        elif self.sheet == 3:
            sheet = "小大"
        elif self.sheet == 4:
            sheet = "大大"
        return sheet


class MatRec(models.Model):
    class Meta:
        verbose_name = "おすすめマットレス"
        verbose_name_plural = "おすすめマットレス"

    id = models.UUIDField(
        "uuid",
        default=uuid4,
        primary_key=True,
        editable=False,
    )
    position1 = models.CharField("位置１", max_length=10)
    position2 = models.CharField("位置２", max_length=10)
    position3 = models.CharField("位置３", max_length=10)
    position4 = models.CharField("位置４", max_length=10)
    position5 = models.CharField("位置５", max_length=10)
    position6 = models.CharField("位置６", max_length=10)
    support_pad1_p = models.IntegerField(
        "サポートパッド1の位置",
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(6)],
    )
    support_pad1_n = models.IntegerField(
        "サポートパッド1の番号",
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(4)],
    )
    support_pad2_p = models.IntegerField(
        "サポートパッド2の位置",
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(6)],
    )
    support_pad2_n = models.IntegerField(
        "サポートパッド2の番号",
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(4)],
    )
    support_pad3_p = models.IntegerField(
        "サポートパッド3の位置",
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(6)],
    )
    support_pad3_n = models.IntegerField(
        "サポートパッド3の番号",
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(4)],
    )
    support_pad4_p = models.IntegerField(
        "サポートパッド4の位置",
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(6)],
    )
    support_pad4_n = models.IntegerField(
        "サポートパッド4の番号",
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(4)],
    )
    created_at = models.DateTimeField("作成日時", auto_now_add=True)


class Hearing(models.Model):
    class Meta:
        verbose_name = "ヒアリング"
        verbose_name_plural = "ヒアリング"

    id = models.UUIDField(
        "uuid",
        default=uuid4,
        primary_key=True,
        editable=False,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sex = models.IntegerField("性別")
    age = models.IntegerField("年齢")
    height = models.FloatField("身長")
    weight = models.FloatField("体重")
    bmi = models.FloatField("BMI")
    both = models.BooleanField("枕とマットレス同時購入")
    question1 = models.TextField("質問１")
    answer1 = models.CharField("回答１", max_length=20)
    question2 = models.TextField("質問２")
    answer2 = models.IntegerField("回答２")
    question3 = models.TextField("質問３")
    answer3 = models.CharField("回答３", max_length=20)
    question4 = models.TextField("質問４")
    answer4 = models.CharField("回答４", max_length=20)
    question5 = models.TextField("質問５")
    answer5 = models.CharField("回答５", max_length=20)
    question6 = models.TextField("質問６")
    answer6 = models.CharField("回答６", max_length=20)
    question7 = models.TextField("質問７")
    answer7 = models.CharField("回答７", max_length=20)
    question8 = models.TextField("質問８")
    answer8 = models.CharField("回答８", max_length=20)
    question9 = models.TextField("質問９")
    answer9 = models.IntegerField("回答９")
    question10 = models.TextField("質問１０")
    answer10 = models.IntegerField("回答１０")
    question11 = models.TextField("質問１１")
    answer11 = models.IntegerField("回答１１")
    question12 = models.TextField("質問１２")
    answer12 = models.CharField("回答１２", max_length=20, null=True)
    question13 = models.TextField("質問１３")
    answer13 = models.IntegerField("回答１３")
    question14 = models.TextField("質問１４")
    answer14 = models.CharField("回答１４", max_length=20, null=True)
    question15 = models.TextField("質問１５")
    answer15 = models.IntegerField("回答１５")
    question16 = models.TextField("質問１６")
    answer16 = models.CharField("回答１６", max_length=20, null=True)
    question17 = models.TextField("質問１７")
    answer17 = models.IntegerField("回答１７")
    question18 = models.TextField("質問１８")
    answer18 = models.CharField("回答１８", max_length=20)
    question19 = models.TextField("質問１９")
    answer19 = models.CharField("回答１９", max_length=20)
    question20 = models.TextField("質問２０")
    answer20 = models.CharField("回答２０", max_length=20)
    question21 = models.TextField("質問２１")
    answer21 = models.CharField("回答２１", max_length=20)
    question22 = models.TextField("質問２２")
    answer22 = models.CharField("回答２２", max_length=20)
    question23 = models.TextField("質問２３")
    answer23 = models.CharField("回答２３", max_length=20)
    question24 = models.TextField("質問２４")
    answer24 = models.CharField("回答２４", max_length=20)
    question25 = models.TextField("質問２５")
    answer25 = models.CharField("回答２５", max_length=20)
    question26 = models.TextField("質問２６")
    answer26 = models.CharField("回答２６", max_length=20, null=True)
    question27 = models.TextField("質問２７")
    answer27 = models.CharField("回答２７", max_length=20)
    question28 = models.TextField("質問２８")
    answer28 = models.CharField("回答２８", max_length=20)
    question29 = models.TextField("質問２９")
    answer29 = models.CharField("回答２９", max_length=20)
    question30 = models.TextField("質問３０")
    answer30 = models.CharField("回答３０", max_length=200, null=True)
    vp_data = models.OneToOneField(Measure, on_delete=models.CASCADE)
    pillow_rec = models.OneToOneField(
        PillowRec,
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )
    mat_rec = models.OneToOneField(
        MatRec,
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    @property
    def sex_jp(self):
        return "男" if self.sex == 1 else "女" if self.sex == 2 else "不明"
