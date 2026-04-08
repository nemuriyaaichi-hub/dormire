from rest_framework.generics import CreateAPIView

from .models import Hearing
from .serializers import HearingSerializer


class RecommendCreateView(CreateAPIView):
    serializer_class = HearingSerializer
    queryset = Hearing.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
