"""Admin pages for espressodb_tests.customizations models

On default generates list view admins for all models
"""
from espressodb.base.admin import register_admins

register_admins("espressodb_tests.customizations", exclude_models=["CA"])
