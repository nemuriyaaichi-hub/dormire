from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from measure.models import MeasureOnly
from users.permissions import IsAdmin, IsSalonUser

from .serializers import MeasureOnlySerializer


class MeasureCreateView(CreateAPIView):
    serializer_class = MeasureOnlySerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsSalonUser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        order_id = serializer.data["id"]
        self.send_email_on_measure(order_id)
        return Response(
            {"status": "OK"},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def send_email_on_measure(self, id):
        measure = MeasureOnly.objects.select_related("user").get(id=id)
        context = {
            "measure": measure,
            "line_url": settings.NEMURIYA_LINE_URL,
            "contact_email": settings.NEMURIYA_CONTACT_EMAIL,
        }
        subject = "【解析診断結果について】Dormire"
        message = render_to_string("measure_mail.html", context=context)
        from_email = settings.NEMURIYA_EMAIL
        recipient_list = [measure.user.email]
        bcc = [settings.NEMURIYA_BCC]
        email = EmailMessage(
            subject,
            message,
            from_email,
            recipient_list,
            bcc,
        )
        email.content_subtype = "html"
        email.send()
