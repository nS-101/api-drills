"""Root URL configuration.

Every exercise lives under its own prefix, e.g. /ex05/notes.
You should not need to edit this file: wire your URLs up in each
exercise's own urls.py instead.
"""
import os

from django.contrib import admin
from django.urls import include, path

# score.py swaps in deliberately broken versions of the ex09 API to check
# whether your tests catch the bugs. Leave this alone.
ex09Urls = os.environ.get("EX09_MUTANT")
ex09Module = f"ex09_write_tests.mutants.{ex09Urls}" if ex09Urls else "ex09_write_tests.urls"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ex03/", include("ex03_basics.urls")),
    path("ex04/", include("ex04_orm.urls")),
    path("ex05/", include("ex05_crud.urls")),
    path("ex06/", include("ex06_mock_oa.urls")),
    path("ex07/", include("ex07_debug_library.urls")),
    path("ex08/", include("ex08_debug_bank.urls")),
    path("ex09/", include(ex09Module)),
    path("ex10/", include("ex10_mock_oa_2.urls")),
]
