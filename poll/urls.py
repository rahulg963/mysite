from django.urls import path
from poll.views import *


urlpatterns = [
    # path('poll/', poll),
    path('poll/', PollAPIView.as_view()),
    path('poll/<int:id>', poll_details),
]

