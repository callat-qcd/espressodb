"""Admin pages for my_app models

On default generates list view admins for all models
"""
from espressodb.base.admin import register_admins

register_admins("my_project.hamiltonian")
