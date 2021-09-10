from django.urls import path
from .views import main

urlpatterns = [
    path('<str:symbol>/<str:min>/<str:max>/<int:minsize>/<int:maxsize>/', main),
    path('<str:symbol>/', main),
]
