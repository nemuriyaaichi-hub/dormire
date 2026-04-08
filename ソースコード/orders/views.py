from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.generics import CreateAPIView

from .models import Order
from .serializers import OrderSerializer


class OrderCreateView(CreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        id = serializer.data["id"]
        self.send_email_on_order(id)

    def send_email_on_order(self, id):
        order = Order.objects.select_related(
            "user", "customer", "pillow_order1", "pillow_order2", "mat_order"
        ).get(id=id)
        cover_count = 0
        cover_count_duo = 0
        if order.pillow_order1:
            pillow1 = order.pillow_order1
            cover_count = pillow1.cover_count
            pillow2 = order.pillow_order2
            cover_count_duo = (
                pillow1.cover_count + pillow2.cover_count if pillow2 else 0
            )

        context = {
            "order": order,
            "line_url": settings.NEMURIYA_LINE_URL,
            "contact_email": settings.NEMURIYA_CONTACT_EMAIL,
            "cover_count": cover_count,
            "cover_count_duo": cover_count_duo,
        }
        subject = "【購入商品の登録について】Dormire"
        message = render_to_string("order_mail.html", context=context)
        from_email = settings.NEMURIYA_EMAIL
        recipient_list = [order.customer.email]
        bcc = [settings.NEMURIYA_BCC]
        email = EmailMessage(subject, message, from_email, recipient_list, bcc)
        email.content_subtype = "html"
        email.send()
