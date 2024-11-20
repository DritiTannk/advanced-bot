from django.urls import path
from .views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    # path('send_message/', send_message, name='send_msg'),
]