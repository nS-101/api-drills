from django.urls import path

from . import views

urlpatterns = [
    path("accounts", views.accountCollection),
    path("accounts/<int:accountId>", views.accountDetail),
    path("accounts/<int:accountId>/deposit", views.deposit),
    path("accounts/<int:accountId>/withdraw", views.withdraw),
    path("transfer", views.transfer),
]
