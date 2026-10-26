from django.urls import path

from . import views

urlpatterns = [
    path("loans", views.loanCollection),
    path("loans/<int:loanId>", views.loanDetail),
    path("loans/<int:loanId>/return/", views.returnLoan),
]
