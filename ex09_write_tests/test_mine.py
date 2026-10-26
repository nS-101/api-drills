from django.test import TestCase


class PriceTests(TestCase):
    def getPrice(self, **params):
        return self.client.get("/ex09/price", params)

    def test_no_coupon(self):
        response = self.getPrice(amount=1000)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"amount": 1000, "discount": 0, "total": 1000})

    # Write your tests below. Each test method name must start with "test".
