from django.urls import path
from bot import views

urlpatterns = [
    path('bot/', views.bot, name="bots"),
    path('list/bot/', views.listBot, name="listBot")
]