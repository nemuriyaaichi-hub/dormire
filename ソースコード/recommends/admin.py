from django.contrib import admin

from .models import Hearing, MatBase, MatRec, PillowBase, PillowRec


class HearingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)


class PillowRecAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
    )
    ordering = ("-created_at",)
    fields = [
        "pillow_rec_sheet",
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
    ]
    readonly_fields = (
        "pillow_rec_sheet",
    )

    @admin.display(description="シート")
    def pillow_rec_sheet(self, obj):
        return obj.con_sheet


class MatRecAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
    )
    ordering = ("-created_at",)


admin.site.register(PillowBase)
admin.site.register(MatBase)
admin.site.register(PillowRec, PillowRecAdmin)
admin.site.register(MatRec, MatRecAdmin)
admin.site.register(Hearing, HearingAdmin)
