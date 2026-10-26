import json

from django.http import HttpResponseNotAllowed, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Account


def accountToDict(account):
    return {"id": account.id, "owner": account.owner, "balance": account.balance, "frozen": account.frozen}


def notFound():
    return JsonResponse({"error": "not found"}, status=404)


def badRequest(message):
    return JsonResponse({"error": message}, status=400)


@csrf_exempt
def accountCollection(request):
    if request.method == "POST":
        data = json.loads(request.body)
        account = Account.objects.create(owner=data["owner"])
        return JsonResponse(accountToDict(account), status=201)
    if request.method == "GET":
        accounts = Account.objects.order_by("balance", "id")
        minBalance = request.GET.get("min_balance")
        if minBalance is not None:
            accounts = accounts.filter(balance__gte=int(minBalance))
        return JsonResponse([accountToDict(a) for a in accounts], safe=False)
    return HttpResponseNotAllowed(["GET", "POST"])


def accountDetail(request, accountId):
    try:
        account = Account.objects.get(id=accountId)
    except Account.DoesNotExist:
        return notFound()
    return JsonResponse(accountToDict(account))


@csrf_exempt
@require_POST
def deposit(request, accountId):
    try:
        account = Account.objects.get(id=accountId)
    except Account.DoesNotExist:
        return notFound()
    amount = json.loads(request.body)["amount"]
    if amount < 0:
        return badRequest("amount must be positive")
    account.balance += amount
    account.save()
    return JsonResponse(accountToDict(account))


@csrf_exempt
@require_POST
def withdraw(request, accountId):
    try:
        account = Account.objects.get(id=accountId)
    except Account.DoesNotExist:
        return notFound()
    amount = json.loads(request.body)["amount"]
    if amount <= 0:
        return badRequest("amount must be positive")
    if account.frozen:
        return badRequest("account is frozen")
    if amount >= account.balance:
        return badRequest("insufficient funds")
    account.balance += amount
    account.save()
    return JsonResponse(accountToDict(account))


@csrf_exempt
@require_POST
def transfer(request):
    data = json.loads(request.body)
    amount = data["amount"]
    if amount <= 0:
        return badRequest("amount must be positive")
    try:
        source = Account.objects.get(id=data["from"])
    except Account.DoesNotExist:
        return notFound()
    if amount > source.balance:
        return badRequest("insufficient funds")
    source.balance -= amount
    source.save()
    try:
        destination = Account.objects.get(id=data["to"])
    except Account.DoesNotExist:
        return notFound()
    destination.balance += amount
    destination.save()
    return JsonResponse({"from": accountToDict(source), "to": accountToDict(destination)})
