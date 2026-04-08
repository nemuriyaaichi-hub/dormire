from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.formats import base_formats

from .utils import generate_password

User = get_user_model()


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        import_id_fields = ("id",)
        fields = (
            "id",
            "email",
            "username",
            "is_crowd_funding_user",
            "is_furusato_tax_user",
            "is_salon_user",
        )

    def after_save_instance(self, user, using_transactions, dry_run):
        if dry_run:
            return
        # password registration
        new_password = generate_password()
        user.set_password(new_password)
        user.save()
        # send email
        subject = "【ユーザー情報の登録について】Dormire"
        message = render_to_string(
            "user_registration_mail.txt",
            context={
                "user": user,
                "password": new_password,
                "line_url": settings.NEMURIYA_LINE_URL,
                "ios_url": settings.DORMIRE_IOS_APP_URL,
                "contact_email": settings.NEMURIYA_CONTACT_EMAIL,
            },
        )
        from_email = settings.NEMURIYA_EMAIL
        recipient_list = [user.email]
        bcc = [settings.NEMURIYA_BCC]
        email = EmailMessage(subject, message, from_email, recipient_list, bcc)
        email.send()


class UserAdmin(ImportExportMixin, UserAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "email",
                    "username",
                    "password",
                    "type",
                )
            },
        ),
        (
            "権限",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_crowd_funding_user",
                    "is_furusato_tax_user",
                    "is_salon_user",
                )
            },
        ),
        (
            "日時",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
        ("有効性", {"fields": ("is_active",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                    "is_crowd_funding_user",
                    "is_furusato_tax_user",
                    "is_salon_user",
                ),
            },
        ),
    )
    list_display = (
        "email",
        "username",
        "is_staff",
    )
    readonly_fields = (
        "id",
        "type",
        "created_at",
        "updated_at",
    )
    list_display_links = (
        "email",
        "username",
    )
    search_fields = (
        "email",
        "username",
    )
    ordering = ("-created_at",)
    resource_class = UserResource

    def get_import_formats(self):
        return (base_formats.CSV,)


admin.site.register(User, UserAdmin)
