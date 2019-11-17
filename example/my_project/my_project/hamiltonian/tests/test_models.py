"""Tests for models specific for the Hamiltonians app
"""
from decimal import Decimal

from mock import patch

from django.test import TestCase

from espressodb.base.exceptions import ConsistencyError
from my_project.hamiltonian.models import Hamiltonian, Contact, Eigenvalue


class EigenvalueTest(TestCase):
    """Tests specific for the Eigenvalue model
    """

    def setUp(self):
        """Creates a hamiltonian for the checks.
        """
        Contact.objects.create(n_sites=10, spacing=Decimal("0.1"), c=Decimal("-1.0"))
        # Store base class to have successful attribute comparison
        self.hamiltonian = Hamiltonian.objects.first()

    def test_save_consistency(self):
        """Tests wether inserting an eigenvalue entry using `save` works as expected.

        Tests:
            1. Save method calls check_consistency with expected arguments
            2. The eigenvalue is properly inserted
        """
        data = {
            "hamiltonian": self.hamiltonian,
            "n_level": 0,
            "value": Decimal("0.0"),
            "tag": None,
        }
        eigenvalue = Eigenvalue(**data)

        with patch.object(Eigenvalue, "check_consistency") as mocked_check_consistency:
            eigenvalue.save(check_consistency=True)

        mocked_check_consistency.assert_called_with(data)

        eigenvalues = Eigenvalue.objects.all()
        self.assertEqual(1, eigenvalues.count())

        stored_eigenvalue = eigenvalues.first()
        for key, value in data.items():
            self.assertEqual(value, getattr(stored_eigenvalue, key))

    def test_save_consistency_fail(self):
        """Calls save such that an `ConsistencyError` is triggered.

        Expects `ConsistencyError` is raised an no eigenvalue is created.
        """
        data = {
            "hamiltonian": self.hamiltonian,
            "n_level": self.hamiltonian.n_sites + 1,
            "value": Decimal("0.0"),
            "tag": None,
        }
        eigenvalue = Eigenvalue(**data)

        with self.assertRaises(ConsistencyError) as context:
            eigenvalue.save()

        self.assertIsInstance(context.exception.error, ValueError)

        eigenvalues = Eigenvalue.objects.all()
        self.assertEqual(0, eigenvalues.count())

    def test_safe_create_consistency(self):
        """Tests wether inserting an eigenvalue entry using `safe_create` works as
        expected.

        Tests:
            1. Save method calls check_consistency with expected arguments
            2. The eigenvalue is properly inserted
        """
        data = {
            "hamiltonian": self.hamiltonian,
            "n_level": 0,
            "value": Decimal("0.0"),
            "tag": None,
        }

        with patch.object(Eigenvalue, "check_consistency") as mocked_check_consistency:
            Eigenvalue.objects.safe_create(**data)

        mocked_check_consistency.assert_called_with(data)

        eigenvalues = Eigenvalue.objects.all()
        self.assertEqual(1, eigenvalues.count())

        stored_eigenvalue = eigenvalues.first()
        for key, value in data.items():
            self.assertEqual(value, getattr(stored_eigenvalue, key))

    def test_safe_create_consistency_fail(self):
        """Calls `safe_create` such that an `ConsistencyError` is triggered.

        Expects `ConsistencyError` is raised an no eigenvalue is created.
        """
        data = {
            "hamiltonian": self.hamiltonian,
            "n_level": self.hamiltonian.n_sites + 1,
            "value": Decimal("0.0"),
            "tag": None,
        }

        with self.assertRaises(ConsistencyError) as context:
            Eigenvalue.objects.safe_create(**data)

        self.assertIsInstance(context.exception.error, ValueError)

        eigenvalues = Eigenvalue.objects.all()
        self.assertEqual(0, eigenvalues.count())
