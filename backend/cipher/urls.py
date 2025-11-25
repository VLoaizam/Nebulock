from django.urls import path

from . import views

app_name = "cipher"

urlpatterns = [
    path("encrypt/", views.encrypt_view, name="encrypt"),
    path("decrypt/", views.decrypt_view, name="decrypt"),
    path("periodic/encrypt/", views.periodic_encrypt_view, name="periodic-encrypt"),
    path("periodic/decrypt/", views.periodic_decrypt_view, name="periodic-decrypt"),
]
