from django.test import TestCase

URL = "/ex07/loans"


def loan(title, member, dueDate):
    return {"book_title": title, "member": member, "due_date": dueDate}


class LoanTestCase(TestCase):
    def post(self, data):
        return self.client.post(URL, data, content_type="application/json")

    def returnLoan(self, loanId):
        return self.client.patch(f"{URL}/{loanId}/return", content_type="application/json")


class CreateTests(LoanTestCase):
    def test_create(self):
        response = self.post(loan("Dune", "Alice", "2026-11-01"))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": 1, "book_title": "Dune", "member": "Alice",
                                           "due_date": "2026-11-01", "returned": False})


class ListTests(LoanTestCase):
    def setUp(self):
        self.post(loan("Dune", "Alice", "2026-11-01"))
        self.post(loan("Emma", "bob", "2026-10-15"))
        self.post(loan("Ulysses", "alice", "2026-10-20"))

    def test_list_ordered_by_id(self):
        self.assertEqual([l["id"] for l in self.client.get(URL).json()], [1, 2, 3])

    def test_member_filter_ignores_case(self):
        self.assertEqual([l["id"] for l in self.client.get(URL, {"member": "ALICE"}).json()], [1, 3])

    def test_overdue_is_strictly_before_and_skips_returned(self):
        self.returnLoan(2)
        response = self.client.get(URL, {"overdue": "true", "as_of": "2026-10-20"})
        # loan 2 is overdue but returned; loan 3 is due *on* 2026-10-20, so not overdue yet
        self.assertEqual(response.json(), [])
        response = self.client.get(URL, {"overdue": "true", "as_of": "2026-10-21"})
        self.assertEqual([l["id"] for l in response.json()], [3])


class DetailTests(LoanTestCase):
    def test_get_one(self):
        self.post(loan("Dune", "Alice", "2026-11-01"))
        self.assertEqual(self.client.get(f"{URL}/1").json()["book_title"], "Dune")

    def test_get_missing(self):
        self.assertEqual(self.client.get(f"{URL}/5").status_code, 404)


class ReturnTests(LoanTestCase):
    def test_return_marks_and_persists(self):
        self.post(loan("Dune", "Alice", "2026-11-01"))
        response = self.returnLoan(1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["returned"])
        self.assertTrue(self.client.get(f"{URL}/1").json()["returned"])

    def test_return_twice_conflicts(self):
        self.post(loan("Dune", "Alice", "2026-11-01"))
        self.returnLoan(1)
        self.assertEqual(self.returnLoan(1).status_code, 409)

    def test_return_missing(self):
        self.assertEqual(self.returnLoan(9).status_code, 404)
