"""Tests for models specific for the Hamiltonians app
"""
from decimal import Decimal

from unittest.mock import patch

from django.forms import ModelForm
from django.test import TestCase

from my_project.hamiltonian.models import Hamiltonian, Contact, Eigenvalue


class EigenValueForm(ModelForm):
    class Meta:
        model = Eigenvalue
        fields = ["hamiltonian", "n_level", "value"]


class EigenvalueTest(TestCase):
    """Tests specific for the Eigenvalue forms
    """

    def setUp(self):
        """Creates a hamiltonian for the checks.
        """
        Contact.objects.create(n_sites=10, spacing=Decimal("0.1"), c=Decimal("-1.0"))
        # Store base class to have successful attribute comparison
        self.hamiltonian = Hamiltonian.objects.first()

    def test_form_checks_consistency(self):
        """Tests wether entering eigenvalue using forms checks consistency.

        Tests:
            1. Form is_valid method calls check_consistency with expected arguments
        """
        data = {
            "hamiltonian": self.hamiltonian.pk,
            "n_level": 0,
            "value": Decimal("0.0"),
        }
        form = EigenValueForm(data)

        with patch.object(Eigenvalue, "check_consistency") as mocked_check_consistency:
            form.is_valid()

        mocked_check_consistency.assert_called()

    def test_form_raises_consistency_error_as_validation_error(self):
        """Tests wether entering eigenvalue using forms checks consistency.

        Tests:
            1. Form is_valid method raises no error if valid
            2. Form is_valid method raises error if inconsistent as validation error
        """
        data = {
            "hamiltonian": self.hamiltonian.pk,
            "n_level": 0,
            "value": Decimal("0.0"),
        }
        form = EigenValueForm(data)
        self.assertTrue(form.is_valid())

        data["n_level"] = 20
        form = EigenValueForm(data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors, {"__all__": ["Eigenstate index larger than matrix allows."]}
        )
