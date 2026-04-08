from django.contrib import admin
from django.utils.html import mark_safe

from .models import Measure, MeasureOnly


class MeasureAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
    )
    ordering = ("-created_at",)


class MeasureOnlyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "kana",
        "created_at",
    )
    search_fields = ("name",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "user",
                ),
            },
        ),
        (
            "計測者情報",
            {
                "fields": (
                    "name",
                    "kana",
                    "phone_number",
                    "email",
                    "post_code",
                    "address",
                    "building",
                ),
            },
        ),
        (
            "計測情報",
            {
                "fields": (
                    "right_arm_length",
                    "left_arm_length",
                    "right_leg_length",
                    "left_leg_length",
                    "knee_ankle",
                    "back_length",
                    "back_angle",
                    "head_angle",
                    "shoulder_angle",
                    "hip_angle",
                    "neck_base",
                    "neck_width",
                    "head_width",
                    "posture",
                    "neck_hip",
                    "hip_knee",
                    "right_shoulder_width",
                    "left_shoulder_width",
                    "right_ear_shoulder",
                    "left_ear_shoulder",
                    "image1_view",
                    "image2_view",
                ),
            },
        ),
        (
            "編集用",
            {
                "fields": (
                    "image1",
                    "image2",
                ),
            },
        ),
    )
    readonly_fields = (
        "id",
        "image1_view",
        "image2_view",
    )
    ordering = ("-created_at",)

    @admin.display(description="VP画像1")
    def image1_view(self, obj):
        return mark_safe(
            f'<img src="{obj.image1.url}" width="800">' if obj.image1 else ""
        )

    @admin.display(description="VP画像2")
    def image2_view(self, obj):
        return mark_safe(
            f'<img src="{obj.image2.url}" width="800">' if obj.image2 else ""
        )


admin.site.register(Measure, MeasureAdmin)
admin.site.register(MeasureOnly, MeasureOnlyAdmin)
