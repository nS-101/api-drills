from django.http import JsonResponse

from .pricing import computePrice


def makePriceView(pricer):
    """Build the /price view around a pricing function (score.py swaps in broken ones)."""

    def priceView(request):
        if request.method != "GET":
            return JsonResponse({"error": "method not allowed"}, status=405)
        try:
            amount = int(request.GET.get("amount", ""))
            result = pricer(amount, request.GET.get("coupon"))
        except ValueError as error:
            return JsonResponse({"error": str(error)}, status=400)
        return JsonResponse(result)

    return priceView
