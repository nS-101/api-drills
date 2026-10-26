from django.test import TestCase

from .models import Account

URL = "/ex08/accounts"


class BankTestCase(TestCase):
    def postJson(self, url, data):
        return self.client.post(url, data, content_type="application/json")

    def makeAccount(self, owner, balance=0, frozen=False):
        account = Account.objects.create(owner=owner, balance=balance, frozen=frozen)
        return account.id

    def balance(self, accountId):
        return Account.objects.get(id=accountId).balance


class AccountTests(BankTestCase):
    def test_create(self):
        response = self.postJson(URL, {"owner": "Alice"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": 1, "owner": "Alice", "balance": 0, "frozen": False})

    def test_get_and_missing(self):
        accountId = self.makeAccount("Alice", 500)
        self.assertEqual(self.client.get(f"{URL}/{accountId}").json()["balance"], 500)
        self.assertEqual(self.client.get(f"{URL}/999").status_code, 404)

    def test_list_highest_balance_first(self):
        a = self.makeAccount("a", 100)
        b = self.makeAccount("b", 900)
        c = self.makeAccount("c", 100)
        self.assertEqual([x["id"] for x in self.client.get(URL).json()], [b, a, c])
        self.assertEqual([x["id"] for x in self.client.get(URL, {"min_balance": "100"}).json()], [b, a, c])
        self.assertEqual([x["id"] for x in self.client.get(URL, {"min_balance": "101"}).json()], [b])


class DepositTests(BankTestCase):
    def test_deposit(self):
        accountId = self.makeAccount("Alice", 100)
        response = self.postJson(f"{URL}/{accountId}/deposit", {"amount": 50})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["balance"], 150)

    def test_deposit_zero_or_negative_rejected(self):
        accountId = self.makeAccount("Alice", 100)
        self.assertEqual(self.postJson(f"{URL}/{accountId}/deposit", {"amount": 0}).status_code, 400)
        self.assertEqual(self.postJson(f"{URL}/{accountId}/deposit", {"amount": -5}).status_code, 400)
        self.assertEqual(self.balance(accountId), 100)


class WithdrawTests(BankTestCase):
    def test_withdraw(self):
        accountId = self.makeAccount("Alice", 100)
        response = self.postJson(f"{URL}/{accountId}/withdraw", {"amount": 30})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.balance(accountId), 70)

    def test_withdraw_whole_balance_allowed(self):
        accountId = self.makeAccount("Alice", 100)
        self.assertEqual(self.postJson(f"{URL}/{accountId}/withdraw", {"amount": 100}).status_code, 200)
        self.assertEqual(self.balance(accountId), 0)

    def test_withdraw_too_much(self):
        accountId = self.makeAccount("Alice", 100)
        self.assertEqual(self.postJson(f"{URL}/{accountId}/withdraw", {"amount": 101}).status_code, 400)
        self.assertEqual(self.balance(accountId), 100)

    def test_withdraw_frozen(self):
        accountId = self.makeAccount("Alice", 100, frozen=True)
        self.assertEqual(self.postJson(f"{URL}/{accountId}/withdraw", {"amount": 10}).status_code, 400)


class TransferTests(BankTestCase):
    def test_transfer(self):
        a = self.makeAccount("a", 100)
        b = self.makeAccount("b", 5)
        response = self.postJson("/ex08/transfer", {"from": a, "to": b, "amount": 60})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["from"]["balance"], 40)
        self.assertEqual(response.json()["to"]["balance"], 65)

    def test_transfer_to_missing_account_changes_nothing(self):
        a = self.makeAccount("a", 100)
        response = self.postJson("/ex08/transfer", {"from": a, "to": 999, "amount": 60})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.balance(a), 100)

    def test_transfer_insufficient(self):
        a = self.makeAccount("a", 10)
        b = self.makeAccount("b", 0)
        self.assertEqual(self.postJson("/ex08/transfer", {"from": a, "to": b, "amount": 11}).status_code, 400)
        self.assertEqual((self.balance(a), self.balance(b)), (10, 0))
