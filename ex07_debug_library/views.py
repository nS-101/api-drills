import json

from django.http import HttpResponseNotAllowed, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Loan


def loanToDict(loan):
    return {
        "id": loan.id,
        "book_title": loan.book_title,
        "member": loan.member,
        "due_date": loan.due_date,
        "returned": loan.returned,
    }


@csrf_exempt
def loanCollection(request):
    if request.method == "POST":
        data = json.loads(request.body)
        loan = Loan.objects.create(
            book_title=data["book_title"],
            member=data["member"],
            due_date=data["due_date"],
        )
        return JsonResponse(loanToDict(loan), status=200)

    if request.method == "GET":
        loans = Loan.objects.order_by("-id")
        member = request.GET.get("member")
        if member:
            loans = loans.filter(member=member)
        if request.GET.get("overdue") == "true":
            asOf = request.GET.get("as_of")
            loans = loans.filter(returned=False, due_date__lte=asOf)
        return JsonResponse([loanToDict(loan) for loan in loans], safe=False)

    return HttpResponseNotAllowed(["GET", "POST"])


def loanDetail(request, loanId):
    loan = Loan.objects.get(id=loanId)
    return JsonResponse(loanToDict(loan))


@csrf_exempt
def returnLoan(request, loanId):
    if request.method != "PATCH":
        return HttpResponseNotAllowed(["PATCH"])
    try:
        loan = Loan.objects.get(id=loanId)
    except Loan.DoesNotExist:
        return JsonResponse({"error": "not found"}, status=404)
    if loan.returned == "true":
        return JsonResponse({"error": "already returned"}, status=409)
    loan.returned = True
    return JsonResponse(loanToDict(loan))
