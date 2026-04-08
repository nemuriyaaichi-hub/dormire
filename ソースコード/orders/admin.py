from django.contrib import admin
from django.utils.html import mark_safe
from django_reverse_admin import ReverseModelAdmin

from .models import Customer, MatOrder, Order, PillowOrder


class OrderInline(admin.StackedInline):
    model = Order
    extra = 1


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone_number",
    )
    search_fields = ["name"]
    inlines = [OrderInline]


class PillowOrderAdmin(ReverseModelAdmin):
    model = PillowOrder
    list_display = (
        "id",
        "created_at",
    )
    ordering = ("-created_at",)
    inline_type = "stacked"
    inline_reverse = ("pillow_rec",)


class MatOrderAdmin(ReverseModelAdmin):
    model = MatOrder
    list_display = (
        "id",
        "created_at",
    )
    ordering = ("-created_at",)
    inline_type = "stacked"
    inline_reverse = ("mat_rec1", "mat_rec2")


class OrderAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "customer",
                "pillow_order1__pillow_rec",
                "pillow_order2__pillow_rec",
                "mat_order__mat_rec1",
                "mat_order__mat_rec2",
            )
        )

    model = Order
    list_display = (
        "id",
        "customer_name",
        "customer_kana",
        "memo",
        "created_at",
    )
    search_fields = ["customer__name"]
    ordering = ("-created_at",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "user",
                    "memo",
                ),
            },
        ),
        (
            "注文者情報",
            {
                "fields": (
                    "customer_name",
                    "customer_kana",
                    "customer_phone_number",
                    "customer_email",
                    "customer_post_code",
                    "customer_address",
                    "customer_building",
                )
            },
        ),
        (
            "マットレスオーダー情報",
            {
                "fields": (
                    "mat_rec1",
                    "mat_rec1_position1",
                    "mat_rec1_position2",
                    "mat_rec1_position3",
                    "mat_rec1_position4",
                    "mat_rec1_position5",
                    "mat_rec1_position6",
                    "mat_rec1_support_pad1_p",
                    "mat_rec1_support_pad1_n",
                    "mat_rec1_support_pad2_p",
                    "mat_rec1_support_pad2_n",
                    "mat_rec1_support_pad3_p",
                    "mat_rec1_support_pad3_n",
                    "mat_rec1_support_pad4_p",
                    "mat_rec1_support_pad4_n",
                    "mat_rec2",
                    "mat_rec2_position1",
                    "mat_rec2_position2",
                    "mat_rec2_position3",
                    "mat_rec2_position4",
                    "mat_rec2_position5",
                    "mat_rec2_position6",
                    "mat_rec2_support_pad1_p",
                    "mat_rec2_support_pad1_n",
                    "mat_rec2_support_pad2_p",
                    "mat_rec2_support_pad2_n",
                    "mat_rec2_support_pad3_p",
                    "mat_rec2_support_pad3_n",
                    "mat_rec2_support_pad4_p",
                    "mat_rec2_support_pad4_n",
                    "mat_size",
                    "mat_thickness",
                    "mat_cover_material",
                    "mat_cover_color1",
                    "mat_cover_color2",
                    "mat_cover_color3",
                )
            },
        ),
        (
            "枕1オーダー情報",
            {
                "fields": (
                    "pillow1_rec",
                    "pillow1_rec_sheet",
                    "pillow1_rec_position1",
                    "pillow1_rec_position2",
                    "pillow1_rec_position3",
                    "pillow1_rec_position4",
                    "pillow1_rec_position5",
                    "pillow1_rec_position6",
                    "pillow1_rec_diff_position1",
                    "pillow1_rec_diff_position2",
                    "pillow1_rec_diff_position3",
                    "pillow1_rec_diff_position4",
                    "pillow1_rec_diff_position5",
                    "pillow1_rec_diff_position6",
                    "pillow1_material",
                    "pillow1_cover_material",
                    "pillow1_cover_color1",
                    "pillow1_cover_color2",
                    "pillow1_cover_color3",
                ),
            },
        ),
        (
            "枕2オーダー情報",
            {
                "fields": (
                    "pillow2_rec",
                    "pillow2_rec_sheet",
                    "pillow2_rec_position1",
                    "pillow2_rec_position2",
                    "pillow2_rec_position3",
                    "pillow2_rec_position4",
                    "pillow2_rec_position5",
                    "pillow2_rec_position6",
                    "pillow2_rec_diff_position1",
                    "pillow2_rec_diff_position2",
                    "pillow2_rec_diff_position3",
                    "pillow2_rec_diff_position4",
                    "pillow2_rec_diff_position5",
                    "pillow2_rec_diff_position6",
                    "pillow2_material",
                    "pillow2_cover_material",
                    "pillow2_cover_color1",
                    "pillow2_cover_color2",
                    "pillow2_cover_color3",
                ),
            },
        ),
        (
            "ヒアリング1情報",
            {
                "fields": (
                    "hearing1_sex",
                    "hearing1_age",
                    "hearing1_height",
                    "hearing1_weight",
                    "hearing1_bmi",
                    "hearing1_question1",
                    "hearing1_answer1",
                    "hearing1_question2",
                    "hearing1_answer2",
                    "hearing1_question3",
                    "hearing1_answer3",
                    "hearing1_question4",
                    "hearing1_answer4",
                    "hearing1_question5",
                    "hearing1_answer5",
                    "hearing1_question6",
                    "hearing1_answer6",
                    "hearing1_question7",
                    "hearing1_answer7",
                    "hearing1_question8",
                    "hearing1_answer8",
                    "hearing1_question9",
                    "hearing1_answer9",
                    "hearing1_question10",
                    "hearing1_answer10",
                    "hearing1_question11",
                    "hearing1_answer11",
                    "hearing1_question12",
                    "hearing1_answer12",
                    "hearing1_question13",
                    "hearing1_answer13",
                    "hearing1_question14",
                    "hearing1_answer14",
                    "hearing1_question15",
                    "hearing1_answer15",
                    "hearing1_question16",
                    "hearing1_answer16",
                    "hearing1_question17",
                    "hearing1_answer17",
                    "hearing1_question18",
                    "hearing1_answer18",
                    "hearing1_question19",
                    "hearing1_answer19",
                    "hearing1_question20",
                    "hearing1_answer20",
                    "hearing1_question21",
                    "hearing1_answer21",
                    "hearing1_question22",
                    "hearing1_answer22",
                    "hearing1_question23",
                    "hearing1_answer23",
                    "hearing1_question24",
                    "hearing1_answer24",
                    "hearing1_question25",
                    "hearing1_answer25",
                    "hearing1_question26",
                    "hearing1_answer26",
                    "hearing1_question27",
                    "hearing1_answer27",
                    "hearing1_question28",
                    "hearing1_answer28",
                    "hearing1_question29",
                    "hearing1_answer29",
                    "hearing1_question30",
                    "hearing1_answer30",
                    "hearing1_vp_data_right_arm_length",
                    "hearing1_vp_data_left_arm_length",
                    "hearing1_vp_data_right_leg_length",
                    "hearing1_vp_data_left_leg_length",
                    "hearing1_vp_data_knee_ankle",
                    "hearing1_vp_data_back_length",
                    "hearing1_vp_data_back_angle",
                    "hearing1_vp_data_head_angle",
                    "hearing1_vp_data_shoulder_angle",
                    "hearing1_vp_data_hip_angle",
                    "hearing1_vp_data_neck_base",
                    "hearing1_vp_data_neck_width",
                    "hearing1_vp_data_head_width",
                    "hearing1_vp_data_posture",
                    "hearing1_vp_data_neck_hip",
                    "hearing1_vp_data_hip_knee",
                    "hearing1_vp_data_right_shoulder_width",
                    "hearing1_vp_data_left_shoulder_width",
                    "hearing1_vp_data_right_ear_shoulder",
                    "hearing1_vp_data_left_ear_shoulder",
                    "hearing1_vp_data_image1",
                    "hearing1_vp_data_image2",
                ),
            },
        ),
        (
            "ヒアリング2情報",
            {
                "fields": (
                    "hearing2_sex",
                    "hearing2_age",
                    "hearing2_height",
                    "hearing2_weight",
                    "hearing2_bmi",
                    "hearing2_question1",
                    "hearing2_answer1",
                    "hearing2_question2",
                    "hearing2_answer2",
                    "hearing2_question3",
                    "hearing2_answer3",
                    "hearing2_question4",
                    "hearing2_answer4",
                    "hearing2_question5",
                    "hearing2_answer5",
                    "hearing2_question6",
                    "hearing2_answer6",
                    "hearing2_question7",
                    "hearing2_answer7",
                    "hearing2_question8",
                    "hearing2_answer8",
                    "hearing2_question9",
                    "hearing2_answer9",
                    "hearing2_question10",
                    "hearing2_answer10",
                    "hearing2_question11",
                    "hearing2_answer11",
                    "hearing2_question12",
                    "hearing2_answer12",
                    "hearing2_question13",
                    "hearing2_answer13",
                    "hearing2_question14",
                    "hearing2_answer14",
                    "hearing2_question15",
                    "hearing2_answer15",
                    "hearing2_question16",
                    "hearing2_answer16",
                    "hearing2_question17",
                    "hearing2_answer17",
                    "hearing2_question18",
                    "hearing2_answer18",
                    "hearing2_question19",
                    "hearing2_answer19",
                    "hearing2_question20",
                    "hearing2_answer20",
                    "hearing2_question21",
                    "hearing2_answer21",
                    "hearing2_question22",
                    "hearing2_answer22",
                    "hearing2_question23",
                    "hearing2_answer23",
                    "hearing2_question24",
                    "hearing2_answer24",
                    "hearing2_question25",
                    "hearing2_answer25",
                    "hearing2_question26",
                    "hearing2_answer26",
                    "hearing2_question27",
                    "hearing2_answer27",
                    "hearing2_question28",
                    "hearing2_answer28",
                    "hearing2_question29",
                    "hearing2_answer29",
                    "hearing2_question30",
                    "hearing2_answer30",
                    "hearing2_vp_data_right_arm_length",
                    "hearing2_vp_data_left_arm_length",
                    "hearing2_vp_data_right_leg_length",
                    "hearing2_vp_data_left_leg_length",
                    "hearing2_vp_data_knee_ankle",
                    "hearing2_vp_data_back_length",
                    "hearing2_vp_data_back_angle",
                    "hearing2_vp_data_head_angle",
                    "hearing2_vp_data_shoulder_angle",
                    "hearing2_vp_data_hip_angle",
                    "hearing2_vp_data_neck_base",
                    "hearing2_vp_data_neck_width",
                    "hearing2_vp_data_head_width",
                    "hearing2_vp_data_posture",
                    "hearing2_vp_data_neck_hip",
                    "hearing2_vp_data_hip_knee",
                    "hearing2_vp_data_right_shoulder_width",
                    "hearing2_vp_data_left_shoulder_width",
                    "hearing2_vp_data_right_ear_shoulder",
                    "hearing2_vp_data_left_ear_shoulder",
                    "hearing2_vp_data_image1",
                    "hearing2_vp_data_image2",
                ),
            },
        ),
        (
            "編集用",
            {
                "fields": (
                    "customer",
                    "mat_order",
                    "pillow_order1",
                    "pillow_order2",
                    "hearing1",
                    "hearing2",
                ),
            },
        ),
    )

    readonly_fields = (
        "id",
        "user",
        "customer_name",
        "customer_kana",
        "customer_phone_number",
        "customer_email",
        "customer_post_code",
        "customer_address",
        "customer_building",
        "mat_rec1",
        "mat_rec1_position1",
        "mat_rec1_position2",
        "mat_rec1_position3",
        "mat_rec1_position4",
        "mat_rec1_position5",
        "mat_rec1_position6",
        "mat_rec1_support_pad1_p",
        "mat_rec1_support_pad1_n",
        "mat_rec1_support_pad2_p",
        "mat_rec1_support_pad2_n",
        "mat_rec1_support_pad3_p",
        "mat_rec1_support_pad3_n",
        "mat_rec1_support_pad4_p",
        "mat_rec1_support_pad4_n",
        "mat_rec2",
        "mat_rec2_position1",
        "mat_rec2_position2",
        "mat_rec2_position3",
        "mat_rec2_position4",
        "mat_rec2_position5",
        "mat_rec2_position6",
        "mat_rec2_support_pad1_p",
        "mat_rec2_support_pad1_n",
        "mat_rec2_support_pad2_p",
        "mat_rec2_support_pad2_n",
        "mat_rec2_support_pad3_p",
        "mat_rec2_support_pad3_n",
        "mat_rec2_support_pad4_p",
        "mat_rec2_support_pad4_n",
        "mat_size",
        "mat_thickness",
        "mat_cover_material",
        "mat_cover_color1",
        "mat_cover_color2",
        "mat_cover_color3",
        "pillow1_rec",
        "pillow1_rec_sheet",
        "pillow1_rec_position1",
        "pillow1_rec_position2",
        "pillow1_rec_position3",
        "pillow1_rec_position4",
        "pillow1_rec_position5",
        "pillow1_rec_position6",
        "pillow1_rec_diff_position1",
        "pillow1_rec_diff_position2",
        "pillow1_rec_diff_position3",
        "pillow1_rec_diff_position4",
        "pillow1_rec_diff_position5",
        "pillow1_rec_diff_position6",
        "pillow1_material",
        "pillow1_cover_material",
        "pillow1_cover_color1",
        "pillow1_cover_color2",
        "pillow1_cover_color3",
        "pillow2_rec",
        "pillow2_rec_sheet",
        "pillow2_rec_position1",
        "pillow2_rec_position2",
        "pillow2_rec_position3",
        "pillow2_rec_position4",
        "pillow2_rec_position5",
        "pillow2_rec_position6",
        "pillow2_rec_diff_position1",
        "pillow2_rec_diff_position2",
        "pillow2_rec_diff_position3",
        "pillow2_rec_diff_position4",
        "pillow2_rec_diff_position5",
        "pillow2_rec_diff_position6",
        "pillow2_material",
        "pillow2_cover_material",
        "pillow2_cover_color1",
        "pillow2_cover_color2",
        "pillow2_cover_color3",
        "hearing1_sex",
        "hearing1_age",
        "hearing1_height",
        "hearing1_weight",
        "hearing1_bmi",
        "hearing1_question1",
        "hearing1_answer1",
        "hearing1_question2",
        "hearing1_answer2",
        "hearing1_question3",
        "hearing1_answer3",
        "hearing1_question4",
        "hearing1_answer4",
        "hearing1_question5",
        "hearing1_answer5",
        "hearing1_question6",
        "hearing1_answer6",
        "hearing1_question7",
        "hearing1_answer7",
        "hearing1_question8",
        "hearing1_answer8",
        "hearing1_question9",
        "hearing1_answer9",
        "hearing1_question10",
        "hearing1_answer10",
        "hearing1_question11",
        "hearing1_answer11",
        "hearing1_question12",
        "hearing1_answer12",
        "hearing1_question13",
        "hearing1_answer13",
        "hearing1_question14",
        "hearing1_answer14",
        "hearing1_question15",
        "hearing1_answer15",
        "hearing1_question16",
        "hearing1_answer16",
        "hearing1_question17",
        "hearing1_answer17",
        "hearing1_question18",
        "hearing1_answer18",
        "hearing1_question19",
        "hearing1_answer19",
        "hearing1_question20",
        "hearing1_answer20",
        "hearing1_question21",
        "hearing1_answer21",
        "hearing1_question22",
        "hearing1_answer22",
        "hearing1_question23",
        "hearing1_answer23",
        "hearing1_question24",
        "hearing1_answer24",
        "hearing1_question25",
        "hearing1_answer25",
        "hearing1_question26",
        "hearing1_answer26",
        "hearing1_question27",
        "hearing1_answer27",
        "hearing1_question28",
        "hearing1_answer28",
        "hearing1_question29",
        "hearing1_answer29",
        "hearing1_question30",
        "hearing1_answer30",
        "hearing1_vp_data_right_arm_length",
        "hearing1_vp_data_left_arm_length",
        "hearing1_vp_data_right_leg_length",
        "hearing1_vp_data_left_leg_length",
        "hearing1_vp_data_knee_ankle",
        "hearing1_vp_data_back_length",
        "hearing1_vp_data_back_angle",
        "hearing1_vp_data_head_angle",
        "hearing1_vp_data_shoulder_angle",
        "hearing1_vp_data_hip_angle",
        "hearing1_vp_data_neck_base",
        "hearing1_vp_data_neck_width",
        "hearing1_vp_data_head_width",
        "hearing1_vp_data_posture",
        "hearing1_vp_data_neck_hip",
        "hearing1_vp_data_hip_knee",
        "hearing1_vp_data_right_shoulder_width",
        "hearing1_vp_data_left_shoulder_width",
        "hearing1_vp_data_right_ear_shoulder",
        "hearing1_vp_data_left_ear_shoulder",
        "hearing1_vp_data_image1",
        "hearing1_vp_data_image2",
        "hearing2_sex",
        "hearing2_age",
        "hearing2_height",
        "hearing2_weight",
        "hearing2_bmi",
        "hearing2_question1",
        "hearing2_answer1",
        "hearing2_question2",
        "hearing2_answer2",
        "hearing2_question3",
        "hearing2_answer3",
        "hearing2_question4",
        "hearing2_answer4",
        "hearing2_question5",
        "hearing2_answer5",
        "hearing2_question6",
        "hearing2_answer6",
        "hearing2_question7",
        "hearing2_answer7",
        "hearing2_question8",
        "hearing2_answer8",
        "hearing2_question9",
        "hearing2_answer9",
        "hearing2_question10",
        "hearing2_answer10",
        "hearing2_question11",
        "hearing2_answer11",
        "hearing2_question12",
        "hearing2_answer12",
        "hearing2_question13",
        "hearing2_answer13",
        "hearing2_question14",
        "hearing2_answer14",
        "hearing2_question15",
        "hearing2_answer15",
        "hearing2_question16",
        "hearing2_answer16",
        "hearing2_question17",
        "hearing2_answer17",
        "hearing2_question18",
        "hearing2_answer18",
        "hearing2_question19",
        "hearing2_answer19",
        "hearing2_question20",
        "hearing2_answer20",
        "hearing2_question21",
        "hearing2_answer21",
        "hearing2_question22",
        "hearing2_answer22",
        "hearing2_question23",
        "hearing2_answer23",
        "hearing2_question24",
        "hearing2_answer24",
        "hearing2_question25",
        "hearing2_answer25",
        "hearing2_question26",
        "hearing2_answer26",
        "hearing2_question27",
        "hearing2_answer27",
        "hearing2_question28",
        "hearing2_answer28",
        "hearing2_question29",
        "hearing2_answer29",
        "hearing2_question30",
        "hearing2_answer30",
        "hearing2_vp_data_right_arm_length",
        "hearing2_vp_data_left_arm_length",
        "hearing2_vp_data_right_leg_length",
        "hearing2_vp_data_left_leg_length",
        "hearing2_vp_data_knee_ankle",
        "hearing2_vp_data_back_length",
        "hearing2_vp_data_back_angle",
        "hearing2_vp_data_head_angle",
        "hearing2_vp_data_shoulder_angle",
        "hearing2_vp_data_hip_angle",
        "hearing2_vp_data_neck_base",
        "hearing2_vp_data_neck_width",
        "hearing2_vp_data_head_width",
        "hearing2_vp_data_posture",
        "hearing2_vp_data_neck_hip",
        "hearing2_vp_data_hip_knee",
        "hearing2_vp_data_right_shoulder_width",
        "hearing2_vp_data_left_shoulder_width",
        "hearing2_vp_data_right_ear_shoulder",
        "hearing2_vp_data_left_ear_shoulder",
        "hearing2_vp_data_image1",
        "hearing2_vp_data_image2",
    )

    @admin.display(description="名前（漢字）")
    def customer_name(self, obj):
        return obj.customer.name

    @admin.display(description="名前（カナ）")
    def customer_kana(self, obj):
        return obj.customer.kana

    @admin.display(description="電話番号")
    def customer_phone_number(self, obj):
        return obj.customer.phone_number

    @admin.display(description="メールアドレス")
    def customer_email(self, obj):
        return obj.customer.email

    @admin.display(description="郵便番号")
    def customer_post_code(self, obj):
        return obj.customer.post_code

    @admin.display(description="住所")
    def customer_address(self, obj):
        return obj.customer.address

    @admin.display(description="建物名")
    def customer_building(self, obj):
        return obj.customer.building

    @admin.display(description="マットレスレコメンド1")
    def mat_rec1(self, obj):
        return obj.mat_order.mat_rec1

    @admin.display(description="マットレス1位置1")
    def mat_rec1_position1(self, obj):
        return obj.mat_order.mat_rec1.position1

    @admin.display(description="マットレス1位置2")
    def mat_rec1_position2(self, obj):
        return obj.mat_order.mat_rec1.position2

    @admin.display(description="マットレス1位置3")
    def mat_rec1_position3(self, obj):
        return obj.mat_order.mat_rec1.position3

    @admin.display(description="マットレス1位置4")
    def mat_rec1_position4(self, obj):
        return obj.mat_order.mat_rec1.position4

    @admin.display(description="マットレス1位置5")
    def mat_rec1_position5(self, obj):
        return obj.mat_order.mat_rec1.position5

    @admin.display(description="マットレス1位置6")
    def mat_rec1_position6(self, obj):
        return obj.mat_order.mat_rec1.position6

    @admin.display(description="マットレス1サポートパッド1位置")
    def mat_rec1_support_pad1_p(self, obj):
        return obj.mat_order.mat_rec1.support_pad1_p

    @admin.display(description="マットレス1サポートパッド1番号")
    def mat_rec1_support_pad1_n(self, obj):
        return obj.mat_order.mat_rec1.support_pad1_n

    @admin.display(description="マットレス1サポートパッド2位置")
    def mat_rec1_support_pad2_p(self, obj):
        return obj.mat_order.mat_rec1.support_pad2_p

    @admin.display(description="マットレス1サポートパッド2番号")
    def mat_rec1_support_pad2_n(self, obj):
        return obj.mat_order.mat_rec1.support_pad2_n

    @admin.display(description="マットレス1サポートパッド3位置")
    def mat_rec1_support_pad3_p(self, obj):
        return obj.mat_order.mat_rec1.support_pad3_p

    @admin.display(description="マットレス1サポートパッド3番号")
    def mat_rec1_support_pad3_n(self, obj):
        return obj.mat_order.mat_rec1.support_pad3_n

    @admin.display(description="マットレス1サポートパッド4位置")
    def mat_rec1_support_pad4_p(self, obj):
        return obj.mat_order.mat_rec1.support_pad4_p

    @admin.display(description="マットレス1サポートパッド4番号")
    def mat_rec1_support_pad4_n(self, obj):
        return obj.mat_order.mat_rec1.support_pad4_n

    @admin.display(description="マットレスレコメンド2")
    def mat_rec2(self, obj):
        return obj.mat_order.mat_rec2

    @admin.display(description="マットレス2位置1")
    def mat_rec2_position1(self, obj):
        return obj.mat_order.mat_rec2.position1

    @admin.display(description="マットレス2位置2")
    def mat_rec2_position2(self, obj):
        return obj.mat_order.mat_rec2.position2

    @admin.display(description="マットレス2位置3")
    def mat_rec2_position3(self, obj):
        return obj.mat_order.mat_rec2.position3

    @admin.display(description="マットレス2位置4")
    def mat_rec2_position4(self, obj):
        return obj.mat_order.mat_rec2.position4

    @admin.display(description="マットレス2位置5")
    def mat_rec2_position5(self, obj):
        return obj.mat_order.mat_rec2.position5

    @admin.display(description="マットレス2位置6")
    def mat_rec2_position6(self, obj):
        return obj.mat_order.mat_rec2.position6

    @admin.display(description="マットレス2サポートパッド1位置")
    def mat_rec2_support_pad1_p(self, obj):
        return obj.mat_order.mat_rec2.support_pad1_p

    @admin.display(description="マットレス2サポートパッド1番号")
    def mat_rec2_support_pad1_n(self, obj):
        return obj.mat_order.mat_rec2.support_pad1_n

    @admin.display(description="マットレス2サポートパッド2位置")
    def mat_rec2_support_pad2_p(self, obj):
        return obj.mat_order.mat_rec2.support_pad2_p

    @admin.display(description="マットレス2サポートパッド2番号")
    def mat_rec2_support_pad2_n(self, obj):
        return obj.mat_order.mat_rec2.support_pad2_n

    @admin.display(description="マットレス2サポートパッド3位置")
    def mat_rec2_support_pad3_p(self, obj):
        return obj.mat_order.mat_rec2.support_pad3_p

    @admin.display(description="マットレス2サポートパッド3番号")
    def mat_rec2_support_pad3_n(self, obj):
        return obj.mat_order.mat_rec2.support_pad3_n

    @admin.display(description="マットレス2サポートパッド4位置")
    def mat_rec2_support_pad4_p(self, obj):
        return obj.mat_order.mat_rec2.support_pad4_p

    @admin.display(description="マットレス2サポートパッド4番号")
    def mat_rec2_support_pad4_n(self, obj):
        return obj.mat_order.mat_rec2.support_pad4_n

    @admin.display(description="マットレスサイズ")
    def mat_size(self, obj):
        return obj.mat_order.size

    @admin.display(description="マットレス厚さ")
    def mat_thickness(self, obj):
        return obj.mat_order.thickness

    @admin.display(description="マットレスカバー素材")
    def mat_cover_material(self, obj):
        return obj.mat_order.cover_material

    @admin.display(description="マットレスカバーグレー")
    def mat_cover_color1(self, obj):
        return obj.mat_order.cover_color1

    @admin.display(description="マットレスカバーベージュ")
    def mat_cover_color2(self, obj):
        return obj.mat_order.cover_color2

    @admin.display(description="マットレスカバーピンク")
    def mat_cover_color3(self, obj):
        return obj.mat_order.cover_color3

    @admin.display(description="枕レコメンド1")
    def pillow1_rec(self, obj):
        return obj.pillow_order1.pillow_rec

    @admin.display(description="枕1シート")
    def pillow1_rec_sheet(self, obj):
        return obj.pillow_order1.pillow_rec.con_sheet

    @admin.display(description="枕1位置1")
    def pillow1_rec_position1(self, obj):
        return obj.pillow_order1.pillow_rec.position1

    @admin.display(description="枕1位置2")
    def pillow1_rec_position2(self, obj):
        return obj.pillow_order1.pillow_rec.position2

    @admin.display(description="枕1位置3")
    def pillow1_rec_position3(self, obj):
        return obj.pillow_order1.pillow_rec.position3

    @admin.display(description="枕1位置4")
    def pillow1_rec_position4(self, obj):
        return obj.pillow_order1.pillow_rec.position4

    @admin.display(description="枕1位置5")
    def pillow1_rec_position5(self, obj):
        return obj.pillow_order1.pillow_rec.position5

    @admin.display(description="枕1位置6")
    def pillow1_rec_position6(self, obj):
        return obj.pillow_order1.pillow_rec.position6

    @admin.display(description="枕1位置1差分")
    def pillow1_rec_diff_position1(self, obj):
        return obj.pillow_order1.pillow_rec.diff_position1

    @admin.display(description="枕1位置2差分")
    def pillow1_rec_diff_position2(self, obj):
        return obj.pillow_order1.pillow_rec.diff_position2

    @admin.display(description="枕1位置3差分")
    def pillow1_rec_diff_position3(self, obj):
        return obj.pillow_order1.pillow_rec.diff_position3

    @admin.display(description="枕1位置4差分")
    def pillow1_rec_diff_position4(self, obj):
        return obj.pillow_order1.pillow_rec.diff_position4

    @admin.display(description="枕1位置5差分")
    def pillow1_rec_diff_position5(self, obj):
        return obj.pillow_order1.pillow_rec.diff_position5

    @admin.display(description="枕1位置6差分")
    def pillow1_rec_diff_position6(self, obj):
        return obj.pillow_order1.pillow_rec.diff_position6

    @admin.display(description="枕1素材")
    def pillow1_material(self, obj):
        return obj.pillow_order1.material

    @admin.display(description="枕1カバー素材")
    def pillow1_cover_material(self, obj):
        return obj.pillow_order1.cover_material

    @admin.display(description="枕1カバーグレー")
    def pillow1_cover_color1(self, obj):
        return obj.pillow_order1.cover_color1

    @admin.display(description="枕1カバーベージュ")
    def pillow1_cover_color2(self, obj):
        return obj.pillow_order1.cover_color2

    @admin.display(description="枕1カバーピンク")
    def pillow1_cover_color3(self, obj):
        return obj.pillow_order1.cover_color3

    @admin.display(description="枕レコメンド2")
    def pillow2_rec(self, obj):
        return obj.pillow_order2.pillow_rec

    @admin.display(description="枕2シート")
    def pillow2_rec_sheet(self, obj):
        return obj.pillow_order2.pillow_rec.con_sheet

    @admin.display(description="枕2位置1")
    def pillow2_rec_position1(self, obj):
        return obj.pillow_order2.pillow_rec.position1

    @admin.display(description="枕2位置2")
    def pillow2_rec_position2(self, obj):
        return obj.pillow_order2.pillow_rec.position2

    @admin.display(description="枕2位置3")
    def pillow2_rec_position3(self, obj):
        return obj.pillow_order2.pillow_rec.position3

    @admin.display(description="枕2位置4")
    def pillow2_rec_position4(self, obj):
        return obj.pillow_order2.pillow_rec.position4

    @admin.display(description="枕2位置5")
    def pillow2_rec_position5(self, obj):
        return obj.pillow_order2.pillow_rec.position5

    @admin.display(description="枕2位置6")
    def pillow2_rec_position6(self, obj):
        return obj.pillow_order2.pillow_rec.position6

    @admin.display(description="枕2位置1差分")
    def pillow2_rec_diff_position1(self, obj):
        return obj.pillow_order2.pillow_rec.diff_position1

    @admin.display(description="枕2位置2差分")
    def pillow2_rec_diff_position2(self, obj):
        return obj.pillow_order2.pillow_rec.diff_position2

    @admin.display(description="枕2位置3差分")
    def pillow2_rec_diff_position3(self, obj):
        return obj.pillow_order2.pillow_rec.diff_position3

    @admin.display(description="枕2位置4差分")
    def pillow2_rec_diff_position4(self, obj):
        return obj.pillow_order2.pillow_rec.diff_position4

    @admin.display(description="枕2位置5差分")
    def pillow2_rec_diff_position5(self, obj):
        return obj.pillow_order2.pillow_rec.diff_position5

    @admin.display(description="枕2位置6差分")
    def pillow2_rec_diff_position6(self, obj):
        return obj.pillow_order2.pillow_rec.diff_position6

    @admin.display(description="枕2素材")
    def pillow2_material(self, obj):
        return obj.pillow_order2.material

    @admin.display(description="枕2カバー素材")
    def pillow2_cover_material(self, obj):
        return obj.pillow_order2.cover_material

    @admin.display(description="枕2カバーグレー")
    def pillow2_cover_color1(self, obj):
        return obj.pillow_order2.cover_color1

    @admin.display(description="枕2カバーベージュ")
    def pillow2_cover_color2(self, obj):
        return obj.pillow_order2.cover_color2

    @admin.display(description="枕2カバーピンク")
    def pillow2_cover_color3(self, obj):
        return obj.pillow_order2.cover_color3

    @admin.display(description="1人目性別")
    def hearing1_sex(self, obj):
        return obj.hearing1.sex_jp

    @admin.display(description="1人目年齢")
    def hearing1_age(self, obj):
        return obj.hearing1.age

    @admin.display(description="1人目身長")
    def hearing1_height(self, obj):
        return obj.hearing1.height

    @admin.display(description="1人目体重")
    def hearing1_weight(self, obj):
        return obj.hearing1.weight

    @admin.display(description="1人目BMI")
    def hearing1_bmi(self, obj):
        return obj.hearing1.bmi

    @admin.display(description="1人目質問1")
    def hearing1_question1(self, obj):
        return obj.hearing1.question1

    @admin.display(description="1人目質問回答2")
    def hearing1_answer1(self, obj):
        return obj.hearing1.answer1

    @admin.display(description="1人目質問2")
    def hearing1_question2(self, obj):
        return obj.hearing1.question2

    @admin.display(description="1人目質問回答2")
    def hearing1_answer2(self, obj):
        return obj.hearing1.answer2

    @admin.display(description="1人目質問3")
    def hearing1_question3(self, obj):
        return obj.hearing1.question3

    @admin.display(description="1人目質問回答3")
    def hearing1_answer3(self, obj):
        return obj.hearing1.answer3

    @admin.display(description="1人目質問4")
    def hearing1_question4(self, obj):
        return obj.hearing1.question4

    @admin.display(description="1人目質問回答4")
    def hearing1_answer4(self, obj):
        return obj.hearing1.answer4

    @admin.display(description="1人目質問5")
    def hearing1_question5(self, obj):
        return obj.hearing1.question5

    @admin.display(description="1人目質問回答5")
    def hearing1_answer5(self, obj):
        return obj.hearing1.answer5

    @admin.display(description="1人目質問6")
    def hearing1_question6(self, obj):
        return obj.hearing1.question6

    @admin.display(description="1人目質問回答6")
    def hearing1_answer6(self, obj):
        return obj.hearing1.answer6

    @admin.display(description="1人目質問7")
    def hearing1_question7(self, obj):
        return obj.hearing1.question7

    @admin.display(description="1人目質問回答7")
    def hearing1_answer7(self, obj):
        return obj.hearing1.answer7

    @admin.display(description="1人目質問8")
    def hearing1_question8(self, obj):
        return obj.hearing1.question8

    @admin.display(description="1人目質問回答8")
    def hearing1_answer8(self, obj):
        return obj.hearing1.answer8

    @admin.display(description="1人目質問9")
    def hearing1_question9(self, obj):
        return obj.hearing1.question9

    @admin.display(description="1人目質問回答9")
    def hearing1_answer9(self, obj):
        return obj.hearing1.answer9

    @admin.display(description="1人目質問10")
    def hearing1_question10(self, obj):
        return obj.hearing1.question10

    @admin.display(description="1人目質問回答10")
    def hearing1_answer10(self, obj):
        return obj.hearing1.answer10

    @admin.display(description="1人目質問11")
    def hearing1_question11(self, obj):
        return obj.hearing1.question11

    @admin.display(description="1人目質問回答11")
    def hearing1_answer11(self, obj):
        return obj.hearing1.answer11

    @admin.display(description="1人目質問12")
    def hearing1_question12(self, obj):
        return obj.hearing1.question12

    @admin.display(description="1人目質問回答12")
    def hearing1_answer12(self, obj):
        return obj.hearing1.answer12

    @admin.display(description="1人目質問13")
    def hearing1_question13(self, obj):
        return obj.hearing1.question13

    @admin.display(description="1人目質問回答13")
    def hearing1_answer13(self, obj):
        return obj.hearing1.answer13

    @admin.display(description="1人目質問14")
    def hearing1_question14(self, obj):
        return obj.hearing1.question14

    @admin.display(description="1人目質問回答14")
    def hearing1_answer14(self, obj):
        return obj.hearing1.answer14

    @admin.display(description="1人目質問15")
    def hearing1_question15(self, obj):
        return obj.hearing1.question15

    @admin.display(description="1人目質問回答15")
    def hearing1_answer15(self, obj):
        return obj.hearing1.answer15

    @admin.display(description="1人目質問16")
    def hearing1_question16(self, obj):
        return obj.hearing1.question16

    @admin.display(description="1人目質問回答16")
    def hearing1_answer16(self, obj):
        return obj.hearing1.answer16

    @admin.display(description="1人目質問17")
    def hearing1_question17(self, obj):
        return obj.hearing1.question17

    @admin.display(description="1人目質問回答17")
    def hearing1_answer17(self, obj):
        return obj.hearing1.answer17

    @admin.display(description="1人目質問18")
    def hearing1_question18(self, obj):
        return obj.hearing1.question18

    @admin.display(description="1人目質問回答18")
    def hearing1_answer18(self, obj):
        return obj.hearing1.answer18

    @admin.display(description="1人目質問19")
    def hearing1_question19(self, obj):
        return obj.hearing1.question19

    @admin.display(description="1人目質問回答19")
    def hearing1_answer19(self, obj):
        return obj.hearing1.answer19

    @admin.display(description="1人目質問20")
    def hearing1_question20(self, obj):
        return obj.hearing1.question20

    @admin.display(description="1人目質問回答20")
    def hearing1_answer20(self, obj):
        return obj.hearing1.answer20

    @admin.display(description="1人目質問21")
    def hearing1_question21(self, obj):
        return obj.hearing1.question21

    @admin.display(description="1人目質問回答21")
    def hearing1_answer21(self, obj):
        return obj.hearing1.answer21

    @admin.display(description="1人目質問22")
    def hearing1_question22(self, obj):
        return obj.hearing1.question22

    @admin.display(description="1人目質問回答22")
    def hearing1_answer22(self, obj):
        return obj.hearing1.answer22

    @admin.display(description="1人目質問23")
    def hearing1_question23(self, obj):
        return obj.hearing1.question23

    @admin.display(description="1人目質問回答23")
    def hearing1_answer23(self, obj):
        return obj.hearing1.answer23

    @admin.display(description="1人目質問24")
    def hearing1_question24(self, obj):
        return obj.hearing1.question24

    @admin.display(description="1人目質問回答24")
    def hearing1_answer24(self, obj):
        return obj.hearing1.answer24

    @admin.display(description="1人目質問25")
    def hearing1_question25(self, obj):
        return obj.hearing1.question25

    @admin.display(description="1人目質問回答25")
    def hearing1_answer25(self, obj):
        return obj.hearing1.answer25

    @admin.display(description="1人目質問26")
    def hearing1_question26(self, obj):
        return obj.hearing1.question26

    @admin.display(description="1人目質問回答26")
    def hearing1_answer26(self, obj):
        return obj.hearing1.answer26

    @admin.display(description="1人目質問27")
    def hearing1_question27(self, obj):
        return obj.hearing1.question27

    @admin.display(description="1人目質問回答27")
    def hearing1_answer27(self, obj):
        return obj.hearing1.answer27

    @admin.display(description="1人目質問28")
    def hearing1_question28(self, obj):
        return obj.hearing1.question28

    @admin.display(description="1人目質問回答28")
    def hearing1_answer28(self, obj):
        return obj.hearing1.answer28

    @admin.display(description="1人目質問29")
    def hearing1_question29(self, obj):
        return obj.hearing1.question29

    @admin.display(description="1人目質問回答29")
    def hearing1_answer29(self, obj):
        return obj.hearing1.answer29

    @admin.display(description="1人目質問30")
    def hearing1_question30(self, obj):
        return obj.hearing1.question30

    @admin.display(description="1人目質問回答30")
    def hearing1_answer30(self, obj):
        return obj.hearing1.answer30

    @admin.display(description="1人目右腕の長さ")
    def hearing1_vp_data_right_arm_length(self, obj):
        return obj.hearing1.vp_data.right_arm_length

    @admin.display(description="1人目左腕の長さ")
    def hearing1_vp_data_left_arm_length(self, obj):
        return obj.hearing1.vp_data.left_arm_length

    @admin.display(description="1人目右足の長さ")
    def hearing1_vp_data_right_leg_length(self, obj):
        return obj.hearing1.vp_data.right_leg_length

    @admin.display(description="1人目左足の長さ")
    def hearing1_vp_data_left_leg_length(self, obj):
        return obj.hearing1.vp_data.left_leg_length

    @admin.display(description="1人目膝から足首までの長さ")
    def hearing1_vp_data_knee_ankle(self, obj):
        return obj.hearing1.vp_data.knee_ankle

    @admin.display(description="1人目背中の長さ")
    def hearing1_vp_data_back_length(self, obj):
        return obj.hearing1.vp_data.back_length

    @admin.display(description="1人目背中の角度")
    def hearing1_vp_data_back_angle(self, obj):
        return obj.hearing1.vp_data.back_angle

    @admin.display(description="1人目頭の傾き")
    def hearing1_vp_data_head_angle(self, obj):
        return obj.hearing1.vp_data.head_angle

    @admin.display(description="1人目肩の角度")
    def hearing1_vp_data_shoulder_angle(self, obj):
        return obj.hearing1.vp_data.shoulder_angle

    @admin.display(description="1人目骨盤の角度")
    def hearing1_vp_data_hip_angle(self, obj):
        return obj.hearing1.vp_data.hip_angle

    @admin.display(description="1人目首の付け根")
    def hearing1_vp_data_neck_base(self, obj):
        return obj.hearing1.vp_data.neck_base

    @admin.display(description="1人目首（首の凹みと付け根の幅）")
    def hearing1_vp_data_neck_width(self, obj):
        return obj.hearing1.vp_data.neck_width

    @admin.display(description="1人目頭（後頭部と付け根の幅）")
    def hearing1_vp_data_head_width(self, obj):
        return obj.hearing1.vp_data.head_width

    @admin.display(description="1人目姿勢診断")
    def hearing1_vp_data_posture(self, obj):
        return obj.hearing1.vp_data.posture

    @admin.display(description="1人目首から骨盤中央までの長さ")
    def hearing1_vp_data_neck_hip(self, obj):
        return obj.hearing1.vp_data.neck_hip

    @admin.display(description="1人目骨盤中央から膝までの長さ")
    def hearing1_vp_data_hip_knee(self, obj):
        return obj.hearing1.vp_data.hip_knee

    @admin.display(description="1人目右半身の肩幅")
    def hearing1_vp_data_right_shoulder_width(self, obj):
        return obj.hearing1.vp_data.right_shoulder_width

    @admin.display(description="1人目左半身の肩幅")
    def hearing1_vp_data_left_shoulder_width(self, obj):
        return obj.hearing1.vp_data.left_shoulder_width

    @admin.display(description="1人目右半身の耳から肩までの長さ")
    def hearing1_vp_data_right_ear_shoulder(self, obj):
        return obj.hearing1.vp_data.right_ear_shoulder

    @admin.display(description="1人目左半身の耳から肩までの長さ")
    def hearing1_vp_data_left_ear_shoulder(self, obj):
        return obj.hearing1.vp_data.left_ear_shoulder

    @admin.display(description="1人目VP画像1")
    def hearing1_vp_data_image1(self, obj):
        return mark_safe(
            f'<img src="{obj.hearing1.vp_data.image1.url}" width="800">'
            if obj.hearing1.vp_data.image1
            else ""
        )

    @admin.display(description="1人目VP画像2")
    def hearing1_vp_data_image2(self, obj):
        return mark_safe(
            f'<img src="{obj.hearing1.vp_data.image2.url}" width="800">'
            if obj.hearing1.vp_data.image2
            else ""
        )

    @admin.display(description="2人目性別")
    def hearing2_sex(self, obj):
        return obj.hearing2.sex_jp

    @admin.display(description="2人目年齢")
    def hearing2_age(self, obj):
        return obj.hearing2.age

    @admin.display(description="2人目身長")
    def hearing2_height(self, obj):
        return obj.hearing2.height

    @admin.display(description="2人目体重")
    def hearing2_weight(self, obj):
        return obj.hearing2.weight

    @admin.display(description="2人目BMI")
    def hearing2_bmi(self, obj):
        return obj.hearing2.bmi

    @admin.display(description="2人目質問1")
    def hearing2_question1(self, obj):
        return obj.hearing2.question1

    @admin.display(description="2人目質問回答2")
    def hearing2_answer1(self, obj):
        return obj.hearing2.answer1

    @admin.display(description="2人目質問2")
    def hearing2_question2(self, obj):
        return obj.hearing2.question2

    @admin.display(description="2人目質問回答2")
    def hearing2_answer2(self, obj):
        return obj.hearing2.answer2

    @admin.display(description="2人目質問3")
    def hearing2_question3(self, obj):
        return obj.hearing2.question3

    @admin.display(description="2人目質問回答3")
    def hearing2_answer3(self, obj):
        return obj.hearing2.answer3

    @admin.display(description="2人目質問4")
    def hearing2_question4(self, obj):
        return obj.hearing2.question4

    @admin.display(description="2人目質問回答4")
    def hearing2_answer4(self, obj):
        return obj.hearing2.answer4

    @admin.display(description="2人目質問5")
    def hearing2_question5(self, obj):
        return obj.hearing2.question5

    @admin.display(description="2人目質問回答5")
    def hearing2_answer5(self, obj):
        return obj.hearing2.answer5

    @admin.display(description="2人目質問6")
    def hearing2_question6(self, obj):
        return obj.hearing2.question6

    @admin.display(description="2人目質問回答6")
    def hearing2_answer6(self, obj):
        return obj.hearing2.answer6

    @admin.display(description="2人目質問7")
    def hearing2_question7(self, obj):
        return obj.hearing2.question7

    @admin.display(description="2人目質問回答7")
    def hearing2_answer7(self, obj):
        return obj.hearing2.answer7

    @admin.display(description="2人目質問8")
    def hearing2_question8(self, obj):
        return obj.hearing2.question8

    @admin.display(description="2人目質問回答8")
    def hearing2_answer8(self, obj):
        return obj.hearing2.answer8

    @admin.display(description="2人目質問9")
    def hearing2_question9(self, obj):
        return obj.hearing2.question9

    @admin.display(description="2人目質問回答9")
    def hearing2_answer9(self, obj):
        return obj.hearing2.answer9

    @admin.display(description="2人目質問10")
    def hearing2_question10(self, obj):
        return obj.hearing2.question10

    @admin.display(description="2人目質問回答10")
    def hearing2_answer10(self, obj):
        return obj.hearing2.answer10

    @admin.display(description="2人目質問11")
    def hearing2_question11(self, obj):
        return obj.hearing2.question11

    @admin.display(description="2人目質問回答11")
    def hearing2_answer11(self, obj):
        return obj.hearing2.answer11

    @admin.display(description="2人目質問12")
    def hearing2_question12(self, obj):
        return obj.hearing2.question12

    @admin.display(description="2人目質問回答12")
    def hearing2_answer12(self, obj):
        return obj.hearing2.answer12

    @admin.display(description="2人目質問13")
    def hearing2_question13(self, obj):
        return obj.hearing2.question13

    @admin.display(description="2人目質問回答13")
    def hearing2_answer13(self, obj):
        return obj.hearing2.answer13

    @admin.display(description="2人目質問14")
    def hearing2_question14(self, obj):
        return obj.hearing2.question14

    @admin.display(description="2人目質問回答14")
    def hearing2_answer14(self, obj):
        return obj.hearing2.answer14

    @admin.display(description="2人目質問15")
    def hearing2_question15(self, obj):
        return obj.hearing2.question15

    @admin.display(description="2人目質問回答15")
    def hearing2_answer15(self, obj):
        return obj.hearing2.answer15

    @admin.display(description="2人目質問16")
    def hearing2_question16(self, obj):
        return obj.hearing2.question16

    @admin.display(description="2人目質問回答16")
    def hearing2_answer16(self, obj):
        return obj.hearing2.answer16

    @admin.display(description="2人目質問17")
    def hearing2_question17(self, obj):
        return obj.hearing2.question17

    @admin.display(description="2人目質問回答17")
    def hearing2_answer17(self, obj):
        return obj.hearing2.answer17

    @admin.display(description="2人目質問18")
    def hearing2_question18(self, obj):
        return obj.hearing2.question18

    @admin.display(description="2人目質問回答18")
    def hearing2_answer18(self, obj):
        return obj.hearing2.answer18

    @admin.display(description="2人目質問19")
    def hearing2_question19(self, obj):
        return obj.hearing2.question19

    @admin.display(description="2人目質問回答19")
    def hearing2_answer19(self, obj):
        return obj.hearing2.answer19

    @admin.display(description="2人目質問20")
    def hearing2_question20(self, obj):
        return obj.hearing2.question20

    @admin.display(description="2人目質問回答20")
    def hearing2_answer20(self, obj):
        return obj.hearing2.answer20

    @admin.display(description="2人目質問21")
    def hearing2_question21(self, obj):
        return obj.hearing2.question21

    @admin.display(description="2人目質問回答21")
    def hearing2_answer21(self, obj):
        return obj.hearing2.answer21

    @admin.display(description="2人目質問22")
    def hearing2_question22(self, obj):
        return obj.hearing2.question22

    @admin.display(description="2人目質問回答22")
    def hearing2_answer22(self, obj):
        return obj.hearing2.answer22

    @admin.display(description="2人目質問23")
    def hearing2_question23(self, obj):
        return obj.hearing2.question23

    @admin.display(description="2人目質問回答23")
    def hearing2_answer23(self, obj):
        return obj.hearing2.answer23

    @admin.display(description="2人目質問24")
    def hearing2_question24(self, obj):
        return obj.hearing2.question24

    @admin.display(description="2人目質問回答24")
    def hearing2_answer24(self, obj):
        return obj.hearing2.answer24

    @admin.display(description="2人目質問25")
    def hearing2_question25(self, obj):
        return obj.hearing2.question25

    @admin.display(description="2人目質問回答25")
    def hearing2_answer25(self, obj):
        return obj.hearing2.answer25

    @admin.display(description="2人目質問26")
    def hearing2_question26(self, obj):
        return obj.hearing2.question26

    @admin.display(description="2人目質問回答26")
    def hearing2_answer26(self, obj):
        return obj.hearing2.answer26

    @admin.display(description="2人目質問27")
    def hearing2_question27(self, obj):
        return obj.hearing2.question27

    @admin.display(description="2人目質問回答27")
    def hearing2_answer27(self, obj):
        return obj.hearing2.answer27

    @admin.display(description="2人目質問28")
    def hearing2_question28(self, obj):
        return obj.hearing2.question28

    @admin.display(description="2人目質問回答28")
    def hearing2_answer28(self, obj):
        return obj.hearing2.answer28

    @admin.display(description="2人目質問29")
    def hearing2_question29(self, obj):
        return obj.hearing2.question29

    @admin.display(description="2人目質問回答29")
    def hearing2_answer29(self, obj):
        return obj.hearing2.answer29

    @admin.display(description="2人目質問30")
    def hearing2_question30(self, obj):
        return obj.hearing2.question30

    @admin.display(description="2人目質問回答30")
    def hearing2_answer30(self, obj):
        return obj.hearing2.answer30

    @admin.display(description="2人目右腕の長さ")
    def hearing2_vp_data_right_arm_length(self, obj):
        return obj.hearing2.vp_data.right_arm_length

    @admin.display(description="2人目左腕の長さ")
    def hearing2_vp_data_left_arm_length(self, obj):
        return obj.hearing2.vp_data.left_arm_length

    @admin.display(description="2人目右足の長さ")
    def hearing2_vp_data_right_leg_length(self, obj):
        return obj.hearing2.vp_data.right_leg_length

    @admin.display(description="2人目左足の長さ")
    def hearing2_vp_data_left_leg_length(self, obj):
        return obj.hearing2.vp_data.left_leg_length

    @admin.display(description="2人目膝から足首までの長さ")
    def hearing2_vp_data_knee_ankle(self, obj):
        return obj.hearing2.vp_data.knee_ankle

    @admin.display(description="2人目背中の長さ")
    def hearing2_vp_data_back_length(self, obj):
        return obj.hearing2.vp_data.back_length

    @admin.display(description="2人目背中の角度")
    def hearing2_vp_data_back_angle(self, obj):
        return obj.hearing2.vp_data.back_angle

    @admin.display(description="2人目頭の傾き")
    def hearing2_vp_data_head_angle(self, obj):
        return obj.hearing2.vp_data.head_angle

    @admin.display(description="2人目肩の角度")
    def hearing2_vp_data_shoulder_angle(self, obj):
        return obj.hearing2.vp_data.shoulder_angle

    @admin.display(description="2人目骨盤の角度")
    def hearing2_vp_data_hip_angle(self, obj):
        return obj.hearing2.vp_data.hip_angle

    @admin.display(description="2人目首の付け根")
    def hearing2_vp_data_neck_base(self, obj):
        return obj.hearing2.vp_data.neck_base

    @admin.display(description="2人目首（首の凹みと付け根の幅）")
    def hearing2_vp_data_neck_width(self, obj):
        return obj.hearing2.vp_data.neck_width

    @admin.display(description="2人目頭（後頭部と付け根の幅）")
    def hearing2_vp_data_head_width(self, obj):
        return obj.hearing2.vp_data.head_width

    @admin.display(description="2人目姿勢診断")
    def hearing2_vp_data_posture(self, obj):
        return obj.hearing2.vp_data.posture

    @admin.display(description="2人目首から骨盤中央までの長さ")
    def hearing2_vp_data_neck_hip(self, obj):
        return obj.hearing2.vp_data.neck_hip

    @admin.display(description="2人目骨盤中央から膝までの長さ")
    def hearing2_vp_data_hip_knee(self, obj):
        return obj.hearing2.vp_data.hip_knee

    @admin.display(description="2人目右半身の肩幅")
    def hearing2_vp_data_right_shoulder_width(self, obj):
        return obj.hearing2.vp_data.right_shoulder_width

    @admin.display(description="2人目左半身の肩幅")
    def hearing2_vp_data_left_shoulder_width(self, obj):
        return obj.hearing2.vp_data.left_shoulder_width

    @admin.display(description="2人目右半身の耳から肩までの長さ")
    def hearing2_vp_data_right_ear_shoulder(self, obj):
        return obj.hearing2.vp_data.right_ear_shoulder

    @admin.display(description="2人目左半身の耳から肩までの長さ")
    def hearing2_vp_data_left_ear_shoulder(self, obj):
        return obj.hearing2.vp_data.left_ear_shoulder

    @admin.display(description="2人目VP画像1")
    def hearing2_vp_data_image1(self, obj):
        return mark_safe(
            f'<img src="{obj.hearing2.vp_data.image1.url}" width="800">'
            if obj.hearing2.vp_data.image1
            else ""
        )

    @admin.display(description="2人目VP画像2")
    def hearing2_vp_data_image2(self, obj):
        return mark_safe(
            f'<img src="{obj.hearing2.vp_data.image2.url}" width="800">'
            if obj.hearing2.vp_data.image2
            else ""
        )


admin.site.register(Order, OrderAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(PillowOrder, PillowOrderAdmin)
admin.site.register(MatOrder, MatOrderAdmin)
