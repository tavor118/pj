"""
This is a django-split-settings main file.
For more information read this:
https://github.com/sobolevn/django-split-settings
https://sobolevn.me/2017/04/managing-djangos-settings
Default environment is `developement`.
To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""

import os

import django_stubs_ext
from split_settings.tools import include, optional  # noqa

# Monkeypatching Django, so stubs will work for all generics,
# see: https://github.com/typeddjango/django-stubs
django_stubs_ext.monkeypatch()

# Managing environment via `DJANGO_ENV` variable:
ENV = os.environ.get("DJANGO_ENV", "development")

base_settings = (
    "components/base.py",
    "components/database.py",
    "components/drf.py",
    "components/logging.py",
    # Select the right env:
    "environments/{0}.py".format(ENV),
)

# Include settings:
include(*base_settings)
