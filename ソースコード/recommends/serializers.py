from decimal import ROUND_HALF_UP, ROUND_UP, Decimal

from rest_framework.exceptions import APIException, ValidationError
from rest_framework.serializers import CharField, IntegerField, ModelSerializer

from measure.models import Measure
from measure.serializers import MeasureSerializer

from .models import Hearing, MatBase, MatRec, PillowBase, PillowRec


class MatRecommendSerializer(ModelSerializer):
    class Meta:
        model = MatRec
        fields = (
            "id",
            "position1",
            "position2",
            "position3",
            "position4",
            "position5",
            "position6",
            "support_pad1_p",
            "support_pad1_n",
            "support_pad2_p",
            "support_pad2_n",
            "support_pad3_p",
            "support_pad3_n",
            "support_pad4_p",
            "support_pad4_n",
        )
        read_only_fields = (
            "id",
            "position1",
            "position2",
            "position3",
            "position4",
            "position5",
            "position6",
            "support_pad1_p",
            "support_pad1_n",
            "support_pad2_p",
            "support_pad2_n",
            "support_pad3_p",
            "support_pad3_n",
            "support_pad4_p",
            "support_pad4_n",
        )


class PillowRecommendSerializer(ModelSerializer):
    class Meta:
        model = PillowRec
        fields = (
            "id",
            "sheet",
            "position1",
            "position2",
            "position3",
            "position4",
            "position5",
            "position6",
            "diff_position1",
            "diff_position2",
            "diff_position3",
            "diff_position4",
            "diff_position5",
            "diff_position6",
        )
        read_only_fields = (
            "id",
            "sheet",
            "position1",
            "position2",
            "position3",
            "position4",
            "position5",
            "position6",
            "diff_position1",
            "diff_position2",
            "diff_position3",
            "diff_position4",
            "diff_position5",
            "diff_position6",
        )


class Hearing1Serializer(ModelSerializer):
    question = CharField(source="question1")
    answer = CharField(source="answer1")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing2Serializer(ModelSerializer):
    question = CharField(source="question2")
    answer = IntegerField(source="answer2")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing3Serializer(ModelSerializer):
    question = CharField(source="question3")
    answer = CharField(source="answer3")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing4Serializer(ModelSerializer):
    question = CharField(source="question4")
    answer = CharField(source="answer4")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing5Serializer(ModelSerializer):
    question = CharField(source="question5")
    answer = CharField(source="answer5")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing6Serializer(ModelSerializer):
    question = CharField(source="question6")
    answer = CharField(source="answer6")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing7Serializer(ModelSerializer):
    question = CharField(source="question7")
    answer = CharField(source="answer7")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing8Serializer(ModelSerializer):
    question = CharField(source="question8")
    answer = CharField(source="answer8")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing9Serializer(ModelSerializer):
    question = CharField(source="question9")
    answer = IntegerField(source="answer9")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing10Serializer(ModelSerializer):
    question = CharField(source="question10")
    answer = IntegerField(source="answer10")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing11Serializer(ModelSerializer):
    question = CharField(source="question11")
    answer = IntegerField(source="answer11")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing12Serializer(ModelSerializer):
    question = CharField(source="question12")
    answer = CharField(source="answer12", allow_null=True)

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing13Serializer(ModelSerializer):
    question = CharField(source="question13")
    answer = IntegerField(source="answer13")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing14Serializer(ModelSerializer):
    question = CharField(source="question14")
    answer = CharField(source="answer14", allow_null=True)

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing15Serializer(ModelSerializer):
    question = CharField(source="question15")
    answer = IntegerField(source="answer15")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing16Serializer(ModelSerializer):
    question = CharField(source="question16")
    answer = CharField(source="answer16", allow_null=True)

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing17Serializer(ModelSerializer):
    question = CharField(source="question17")
    answer = IntegerField(source="answer17")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing18Serializer(ModelSerializer):
    question = CharField(source="question18")
    answer = CharField(source="answer18")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing19Serializer(ModelSerializer):
    question = CharField(source="question19")
    answer = CharField(source="answer19")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing20Serializer(ModelSerializer):
    question = CharField(source="question20")
    answer = CharField(source="answer20")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing21Serializer(ModelSerializer):
    question = CharField(source="question21")
    answer = CharField(source="answer21")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing22Serializer(ModelSerializer):
    question = CharField(source="question22")
    answer = CharField(source="answer22")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing23Serializer(ModelSerializer):
    question = CharField(source="question23")
    answer = CharField(source="answer23")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing24Serializer(ModelSerializer):
    question = CharField(source="question24")
    answer = CharField(source="answer24")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing25Serializer(ModelSerializer):
    question = CharField(source="question25")
    answer = CharField(source="answer25")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing26Serializer(ModelSerializer):
    question = CharField(source="question26")
    answer = CharField(source="answer26", allow_null=True)

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing27Serializer(ModelSerializer):
    question = CharField(source="question27")
    answer = CharField(source="answer27")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing28Serializer(ModelSerializer):
    question = CharField(source="question28")
    answer = CharField(source="answer28")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing29Serializer(ModelSerializer):
    question = CharField(source="question29")
    answer = CharField(source="answer29")

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class Hearing30Serializer(ModelSerializer):
    question = CharField(source="question30")
    answer = CharField(source="answer30", allow_null=True)

    class Meta:
        model = Hearing
        fields = (
            "question",
            "answer",
        )


class HearingSerializer(ModelSerializer):
    mat_rec = MatRecommendSerializer(read_only=True)
    pillow_rec = PillowRecommendSerializer(read_only=True)
    vp_data = MeasureSerializer(write_only=True)
    hearing1 = Hearing1Serializer(write_only=True, source="*")
    hearing2 = Hearing2Serializer(write_only=True, source="*")
    hearing3 = Hearing3Serializer(write_only=True, source="*")
    hearing4 = Hearing4Serializer(write_only=True, source="*")
    hearing5 = Hearing5Serializer(write_only=True, source="*")
    hearing6 = Hearing6Serializer(write_only=True, source="*")
    hearing7 = Hearing7Serializer(write_only=True, source="*")
    hearing8 = Hearing8Serializer(write_only=True, source="*")
    hearing9 = Hearing9Serializer(write_only=True, source="*")
    hearing10 = Hearing10Serializer(write_only=True, source="*")
    hearing11 = Hearing11Serializer(write_only=True, source="*")
    hearing12 = Hearing12Serializer(write_only=True, source="*")
    hearing13 = Hearing13Serializer(write_only=True, source="*")
    hearing14 = Hearing14Serializer(write_only=True, source="*")
    hearing15 = Hearing15Serializer(write_only=True, source="*")
    hearing16 = Hearing16Serializer(write_only=True, source="*")
    hearing17 = Hearing17Serializer(write_only=True, source="*")
    hearing18 = Hearing18Serializer(write_only=True, source="*")
    hearing19 = Hearing19Serializer(write_only=True, source="*")
    hearing20 = Hearing20Serializer(write_only=True, source="*")
    hearing21 = Hearing21Serializer(write_only=True, source="*")
    hearing22 = Hearing22Serializer(write_only=True, source="*")
    hearing23 = Hearing23Serializer(write_only=True, source="*")
    hearing24 = Hearing24Serializer(write_only=True, source="*")
    hearing25 = Hearing25Serializer(write_only=True, source="*")
    hearing26 = Hearing26Serializer(write_only=True, source="*")
    hearing27 = Hearing27Serializer(write_only=True, source="*")
    hearing28 = Hearing28Serializer(write_only=True, source="*")
    hearing29 = Hearing29Serializer(write_only=True, source="*")
    hearing30 = Hearing30Serializer(write_only=True, source="*")

    class Meta:
        model = Hearing
        fields = (
            "sex",
            "age",
            "height",
            "weight",
            "both",
            "hearing1",
            "hearing2",
            "hearing3",
            "hearing4",
            "hearing5",
            "hearing6",
            "hearing7",
            "hearing8",
            "hearing9",
            "hearing10",
            "hearing11",
            "hearing12",
            "hearing13",
            "hearing14",
            "hearing15",
            "hearing16",
            "hearing17",
            "hearing18",
            "hearing19",
            "hearing20",
            "hearing21",
            "hearing22",
            "hearing23",
            "hearing24",
            "hearing25",
            "hearing26",
            "hearing27",
            "hearing28",
            "hearing29",
            "hearing30",
            "vp_data",
            "mat_rec",
            "pillow_rec",
        )

        extra_kwargs = {
            "sex": {"write_only": True},
            "age": {"write_only": True},
            "height": {"write_only": True},
            "weight": {"write_only": True},
            "both": {"write_only": True},
        }

    def calc_bmi(self, height, weight):
        return weight / (height / 100) ** 2

    def generate_recommend_support_pad_place_by_data(self, validated_data, is_u_type):
        vp_data = validated_data["vp_data"]
        place = []
        hip_place_f = 20 + vp_data.neck_hip
        hip_place = Decimal(hip_place_f).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        knee_place_f = hip_place_f + vp_data.hip_knee
        knee_place = Decimal(knee_place_f).quantize(
            Decimal("1"), rounding=ROUND_HALF_UP
        )
        ankle_place_f = knee_place_f + vp_data.knee_ankle
        ankle_place = Decimal(ankle_place_f).quantize(
            Decimal("1"), rounding=ROUND_HALF_UP
        )
        have_warped_waist = is_u_type or (validated_data["answer20"] in ["ある", "少しある"])

        # 骨盤位置
        if 63 <= hip_place <= 71:
            place.append([3, 1])
        elif 72 <= hip_place <= 80:
            place.append([3, 2])
        elif 81 <= hip_place <= 88:
            place.append([3, 3])
        elif 89 <= hip_place <= 96:
            place.append([3, 4])
        elif 97 <= hip_place <= 105:
            place.append([4, 1])
        elif 106 <= hip_place <= 114:
            place.append([4, 2])
        elif 115 <= hip_place <= 123:
            place.append([4, 3])
        elif 124 <= hip_place <= 132:
            place.append([4, 4])
        if have_warped_waist and len(place) >= 1:
            p = place[-1][0]
            n = place[-1][1] - 1
            if n == 0:
                p -= 1
                n = 4
            place.append([p, n])

        # 膝位置
        if 97 <= knee_place <= 105:
            place.append([4, 1])
        elif 106 <= knee_place <= 114:
            place.append([4, 2])
        elif 115 <= knee_place <= 123:
            place.append([4, 3])
        elif 124 <= knee_place <= 133:
            place.append([4, 4])
        elif 134 <= knee_place <= 141:
            place.append([5, 1])
        elif 142 <= knee_place <= 150:
            place.append([5, 2])
        elif 151 <= knee_place <= 159:
            place.append([5, 3])
        elif 160 <= knee_place <= 168:
            place.append([5, 4])

        # 足首位置
        if 134 <= ankle_place <= 142:
            place.append([5, 1])
        elif 143 <= ankle_place <= 151:
            place.append([5, 2])
        elif 152 <= ankle_place <= 160:
            place.append([5, 3])
        elif 161 <= ankle_place <= 168:
            place.append([5, 4])
        elif 169 <= ankle_place <= 176:
            place.append([6, 1])
        elif 177 <= ankle_place <= 184:
            place.append([6, 2])
        elif 185 <= ankle_place <= 192:
            place.append([6, 3])
        elif 193 <= ankle_place:
            raise ValidationError("足首位置が上限を超えています")

        if len(place) > 4:
            raise APIException("サポートパッドが4つを超過しています")

        place.sort(key=lambda x: x[0] * 10 + x[1])
        return place

    # データからおすすめマットレスを作成
    def generate_recommend_mat_by_data(self, validated_data, bmi):
        # 値map
        hardness_map = {
            "かなり柔らかい": 1,
            "柔らかい": 2,
            "普通": 3,
            "硬め": 4,
            "かなり硬め": 5,
        }
        # 身長
        height = Decimal(validated_data["height"]).quantize(
            Decimal("0"), rounding=ROUND_HALF_UP
        )
        # SELECT実行
        mat_base_queryset = MatBase.objects.filter(
            height_min__lte=height,
            height_max__gte=height,
            bmi_min__lte=bmi,
            bmi_max__gte=bmi,
            sex=validated_data["sex"],
            have_backache=(validated_data["answer15"] >= 3),
            have_shoulder_pain=(validated_data["answer13"] >= 3),
            hardness=hardness_map[validated_data["answer24"]],
            posture=validated_data["vp_data"].posture,
        )
        if mat_base_queryset.count() != 1:
            raise ValidationError("マットレスのおすすめができませんでした")

        mat_base = mat_base_queryset.get()

        # 値コピーし，サポートパッド情報を足してレコメンドインスタンスを作成し返す
        mat_rec = MatRec.objects.create(
            position1=mat_base.position1,
            position2=mat_base.position2,
            position3=mat_base.position3,
            position4=mat_base.position4,
            position5=mat_base.position5,
            position6=mat_base.position6,
        )

        place = self.generate_recommend_support_pad_place_by_data(
            validated_data,
            validated_data["vp_data"].posture == "U",
        )
        for i, p in enumerate(place):
            setattr(mat_rec, f"support_pad{i+1}_p", p[0])
            setattr(mat_rec, f"support_pad{i+1}_n", p[1])
        mat_rec.save()
        return mat_rec

    # 枕ロジック用小数処理関数
    def decimal_proc(self, position):
        if position > 0:
            pn = 1
        elif position < 0:
            pn = -1
        position = Decimal(abs(position)).quantize(
            Decimal("0.1"), rounding=ROUND_HALF_UP
        )
        i = int(position)
        if i < position <= i + 0.5:
            position = (i + 0.5) * pn
        elif i + 0.5 < position < i + 1:
            position = (i + 1) * pn
        else:
            position = i
        # 例外処理
        d = abs(position) - abs(int(position))
        if d != 0 and d != 0.5:
            raise ValidationError("小数処理に失敗しました")
        return position

    # 枕ロジック用BMI関数
    def calc_pillow_height_by_bmi(self, pillow, bmi):
        for i, position in enumerate(pillow):
            if i == 0 or i == 1:
                if bmi <= 19.0:
                    position -= 0.5
                elif 19.1 <= bmi <= 20.9:
                    position -= 0.25
                elif 21.0 <= bmi <= 23.9:
                    position -= 0
                elif 24.0 <= bmi <= 25.4:
                    position += 0
                elif 25.5 <= bmi <= 27.0:
                    position += 0.25
                elif 27.1 <= bmi:
                    position += 0.5
            else:
                if bmi <= 19.0:
                    position -= 0.75
                elif 19.1 <= bmi <= 20.9:
                    position -= 0.5
                elif 21.0 <= bmi <= 23.9:
                    position -= 0.25
                elif 24.0 <= bmi <= 25.4:
                    position += 0
                elif 25.5 <= bmi <= 27.0:
                    position += 0.25
                elif 27.1 <= bmi:
                    position += 0.5
            pillow[i] = position
        return

    # 枕の高さを算出する関数
    def calc_pillow_height(self, pillow, validated_data, bmi):
        # 前処理
        vp_data = validated_data["vp_data"]
        shoulder_angle = Decimal(vp_data.shoulder_angle).quantize(
            Decimal("0"), rounding=ROUND_HALF_UP
        )
        # 初期値
        position1 = 5.5 - vp_data.neck_width
        position2 = 10.5 - vp_data.head_width
        position3 = vp_data.right_shoulder_width - 5.5
        position4 = vp_data.right_ear_shoulder - 2.5
        position5 = vp_data.left_shoulder_width - 5.5
        position6 = vp_data.left_ear_shoulder - 2.5
        # ヒアリング及びVPデータから算出
        if validated_data["answer13"] >= 3:
            if validated_data["answer14"] == "右":
                position3 += 0.5
            elif validated_data["answer14"] == "左":
                position5 += 0.5
            elif validated_data["answer14"] == "左右":
                position3 += 0.5
                position5 += 0.5
        if validated_data["answer27"] == "高め":
            position1 += 0.5
            position2 += 0.5
            position3 += 0.5
            position4 += 0.5
            position5 += 0.5
            position6 += 0.5
        if validated_data["answer27"] == "かなり高め":
            position1 += 1
            position2 += 1
            position3 += 1
            position4 += 1
            position5 += 1
            position6 += 1
        if validated_data["answer27"] == "低め":
            position1 -= 0.5
            position2 -= 0.5
            position3 -= 0.5
            position4 -= 0.5
            position5 -= 0.5
            position6 -= 0.5
        if validated_data["answer27"] == "かなり低め":
            position1 -= 1
            position2 -= 1
            position3 -= 1
            position4 -= 1
            position5 -= 1
            position6 -= 1
        if not validated_data["both"]:
            if validated_data["answer23"] == "かなり柔らかい":
                position1 -= 0.5
                position2 -= 0.5
                position3 -= 0.5
                position4 -= 0.5
                position5 -= 0.5
                position6 -= 0.5
            if validated_data["answer23"] == "柔らかい":
                position1 -= 0.25
                position2 -= 0.25
                position3 -= 0.25
                position4 -= 0.25
                position5 -= 0.25
                position6 -= 0.25
            if validated_data["answer23"] == "かなり硬め":
                position1 += 0.5
                position2 += 0.5
                position3 += 0.5
                position4 += 0.5
                position5 += 0.5
                position6 += 0.5
            if validated_data["answer23"] == "硬め":
                position1 += 0.25
                position2 += 0.25
                position3 += 0.25
                position4 += 0.25
                position5 += 0.25
                position6 += 0.25
        if validated_data["both"]:
            position1 -= 0.25
            position2 -= 0.25
            position3 -= 0.5
            position4 -= 0.5
            position5 -= 0.5
            position6 -= 0.5
        if 27 <= shoulder_angle:
            position3 -= 1
            position4 -= 1
            position5 -= 1
            position6 -= 1
        if 24 <= shoulder_angle <= 26:
            position3 -= 0.5
            position4 -= 0.5
            position5 -= 0.5
            position6 -= 0.5
        if shoulder_angle <= 18:
            position3 += 1
            position4 += 1
            position5 += 1
            position6 += 1
        if 19 <= shoulder_angle <= 21:
            position3 += 0.5
            position4 += 0.5
            position5 += 0.5
            position6 += 0.5
        if validated_data["age"] >= 65:
            position1 -= 0.25
            position2 -= 0.25
            position3 -= 0.5
            position4 -= 0.5
            position5 -= 0.5
            position6 -= 0.5
        if validated_data["age"] < 16:
            position1 -= 0.25
            position2 -= 0.25
            position3 -= 0.25
            position4 -= 0.25
            position5 -= 0.25
            position6 -= 0.25
        if vp_data.posture == "W":
            position1 += 0.25
            position3 += 0.25
            position5 += 0.25
        if vp_data.posture == "丸":
            position1 += 0.25
            position3 += 0.25
            position5 += 0.25
        if vp_data.posture == "U":
            position1 -= 0.25
            position2 -= 0.25
            position4 -= 0.25
            position6 -= 0.25
        if validated_data["sex"] == 2:
            position1 -= 0.25
            position2 -= 0.25
            position3 -= 0.25
            position4 -= 0.25
            position5 -= 0.25
            position6 -= 0.25
        if validated_data["answer28"] == "支えたい":
            position1 += 0.25
            position3 += 0.25
            position5 += 0.25
        if validated_data["answer28"] == "支えたくない":
            position1 -= 0.25
            position3 -= 0.25
            position5 -= 0.25
        if validated_data["answer18"] == "よくある":
            position1 += 0.5
            position3 += 0.5
            position5 += 0.5
        if validated_data["answer18"] == "たまにある":
            position1 += 0.25
            position3 += 0.25
            position5 += 0.25
        if validated_data["answer11"] >= 3:
            if validated_data["answer12"] == "右":
                position3 -= 0.25
                position4 -= 0.25
            elif validated_data["answer12"] == "左":
                position5 -= 0.25
                position6 -= 0.25
            elif validated_data["answer12"] == "左右":
                position3 -= 0.25
                position4 -= 0.25
                position5 -= 0.25
                position6 -= 0.25
        pillow.extend(
            [position1, position2, position3, position4, position5, position6]
        )
        # BMIから算出
        self.calc_pillow_height_by_bmi(pillow, bmi)
        # 小数処理
        for i, position in enumerate(pillow):
            position_re = self.decimal_proc(position)
            # 範囲外の値を処理
            if i == 0:
                if position_re < 4:
                    position_re = 4
                elif 13.5 < position_re:
                    position_re = 13.5
            elif i == 1:
                if position_re < 4:
                    position_re = 4
                elif 12 < position_re:
                    position_re = 12
            else:
                if position_re < 4.5:
                    position_re = 4.5
                elif 14.5 < position_re:
                    position_re = 14.5
            pillow[i] = position_re
        return

    # シートの厚みを算出する関数
    def calc_pillow_sheet(self, position1):
        if 4 <= position1 <= 6.5:
            sheet = 1
        elif 7 <= position1 <= 8:
            sheet = 2
        elif 8.5 <= position1 <= 10.5:
            sheet = 3
        elif 11 <= position1 <= 13.5:
            sheet = 4
        else:
            raise ValidationError("枕シートを決定できませんでした")
        return sheet

    # 枕の単位変換（例外：備長炭パイプ）用関数
    def convert_pillow_unit_ex(self, pillow):
        for i, position in enumerate(pillow):
            if position < 0:
                position = Decimal(position * 1.05).quantize(
                    Decimal("0"), rounding=ROUND_UP
                )
            elif position > 0:
                position = Decimal(position * 0.95).quantize(
                    Decimal("0"), rounding=ROUND_UP
                )
            pillow[i] = position
        return

    # 枕の単位変換用関数
    def convert_pillow_unit(self, sheet, pillow, material):
        # 位置１用マップ
        unit_map_1 = {
            4: -120,
            4.5: -100,
            5: -80,
            5.5: -60,
            6: -40,
            6.5: -20,
            7: -40,
            7.5: -20,
            8: 0,
            8.5: -20,
            9: 0,
            9.5: 20,
            10: 40,
            10.5: 60,
            11: 40,
            11.5: 60,
            12: 80,
            12.5: 100,
            13: 120,
            13.5: 140,
        }
        if sheet == 1:
            pillow[0] = unit_map_1[pillow[0]]
            pillow[1] = (pillow[1] - 4) * 50 - 150
            pillow[2] = (pillow[2] - 4.5) * 40 - 100
            pillow[3] = (pillow[3] - 4.5) * 60 - 210
            pillow[4] = (pillow[4] - 4.5) * 40 - 100
            pillow[5] = (pillow[5] - 4.5) * 60 - 210
        elif sheet == 2:
            pillow[0] = unit_map_1[pillow[0]]
            pillow[1] = (pillow[1] - 4) * 50 - 200
            pillow[2] = (pillow[2] - 4.5) * 40 - 140
            pillow[3] = (pillow[3] - 4.5) * 60 - 270
            pillow[4] = (pillow[4] - 4.5) * 40 - 140
            pillow[5] = (pillow[5] - 4.5) * 60 - 270
        elif sheet == 3:
            pillow[0] = unit_map_1[pillow[0]]
            pillow[1] = max((pillow[1] - 5), 0) * 50 - 200
            pillow[2] = (pillow[2] - 4.5) * 40 - 180
            if pillow[3] <= 4.5:
                pillow[3] = -310
            else:
                pillow[3] = (pillow[3] - 5) * 60 - 300
            pillow[4] = (pillow[4] - 4.5) * 40 - 180
            if pillow[5] <= 4.5:
                pillow[5] = -310
            else:
                pillow[5] = (pillow[5] - 5) * 60 - 300
        elif sheet == 4:
            pillow[0] = unit_map_1[pillow[0]]
            pillow[1] = max((pillow[1] - 6), 0) * 50 - 200
            pillow[2] = max((pillow[2] - 5.5), 0) * 40 - 180
            if pillow[3] <= 5.5:
                pillow[3] = -310
            else:
                pillow[3] = (pillow[3] - 6) * 60 - 300
            pillow[4] = max((pillow[4] - 5.5), 0) * 40 - 180
            if pillow[5] <= 5.5:
                pillow[5] = -310
            else:
                pillow[5] = (pillow[5] - 6) * 60 - 300
        # 素材が備長炭パイプの場合
        if material == "備長炭パイプ":
            self.convert_pillow_unit_ex(pillow)
        return

    # データからおすすめ枕を作成
    def generate_recommend_pillow_by_data(self, validated_data, bmi):
        # 枕素材
        material = validated_data["answer29"]
        if material not in ["ソフトパイプ", "エラストマーパイプ", "備長炭パイプ"]:
            raise ValidationError("枕素材はソフトパイプ・エラストマーパイプ・備長炭パイプのいずれかを指定してください")
        # 枕の位置リスト
        pillow = []
        # 枕の高さを算出
        self.calc_pillow_height(pillow, validated_data, bmi)
        # 枕シートを決定
        sheet = self.calc_pillow_sheet(pillow[0])
        # 枕の高さをgに変換
        self.convert_pillow_unit(sheet, pillow, material)
        # 特定の枕素材の通常時の高さを取得
        pillow_base_queryset = PillowBase.objects.filter(
            material=material,
        )
        # 例外処理
        if pillow_base_queryset.count() != 1:
            raise ValidationError("枕のおすすめができませんでした")
        pillow_base = pillow_base_queryset.get()
        # 枕のおすすめを作成
        pillow_rec = PillowRec.objects.create(
            sheet=sheet,
            position1=pillow[0] + pillow_base.position1,
            position2=pillow[1] + pillow_base.position2,
            position3=pillow[2] + pillow_base.position3,
            position4=pillow[3] + pillow_base.position4,
            position5=pillow[4] + pillow_base.position5,
            position6=pillow[5] + pillow_base.position6,
            diff_position1=pillow[0],
            diff_position2=pillow[1],
            diff_position3=pillow[2],
            diff_position4=pillow[3],
            diff_position5=pillow[4],
            diff_position6=pillow[5],
        )
        return pillow_rec

    def create(self, validated_data):
        vp_data = validated_data.pop("vp_data")
        vp_data["user"] = self.context["request"].user
        validated_data["vp_data"] = Measure.objects.create(**vp_data)

        bmi_f = self.calc_bmi(validated_data["height"], validated_data["weight"])
        bmi = Decimal(bmi_f).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        validated_data["bmi"] = bmi

        validated_data["mat_rec"] = self.generate_recommend_mat_by_data(
            validated_data, bmi
        )
        validated_data["pillow_rec"] = self.generate_recommend_pillow_by_data(
            validated_data, bmi
        )

        return super().create(validated_data)
