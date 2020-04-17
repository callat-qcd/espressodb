"""Tests for models specific for the Hamiltonians app
"""
from decimal import Decimal

from unittest.mock import patch

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
            eigenvalue.save()

        mocked_check_consistency.assert_called()

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

    def test_create_consistency(self):
        """Tests wether inserting an eigenvalue entry using `create` works as
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
            Eigenvalue.objects.create(**data)

        mocked_check_consistency.assert_called()

        eigenvalues = Eigenvalue.objects.all()
        self.assertEqual(1, eigenvalues.count())

        stored_eigenvalue = eigenvalues.first()
        for key, value in data.items():
            self.assertEqual(value, getattr(stored_eigenvalue, key))

    def test_create_consistency_fail(self):
        """Calls `create` such that an `ConsistencyError` is triggered.

        Expects `ConsistencyError` is raised an no eigenvalue is created.
        """
        data = {
            "hamiltonian": self.hamiltonian,
            "n_level": self.hamiltonian.n_sites + 1,
            "value": Decimal("0.0"),
            "tag": None,
        }

        with self.assertRaises(ConsistencyError) as context:
            Eigenvalue.objects.create(**data)

        self.assertIsInstance(context.exception.error, ValueError)

        eigenvalues = Eigenvalue.objects.all()
        self.assertEqual(0, eigenvalues.count())

    def test_get_or_create_consistency(self):
        """Tests wether inserting an eigenvalue entry using `get_or_create` works as
        expected.

        Also checks if calling this method twice with the same input returns the same
        eigenvalue entry.

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
            ev, created = Eigenvalue.objects.get_or_create(**data)

        self.assertTrue(created)
        mocked_check_consistency.assert_called()

        eigenvalues = Eigenvalue.objects.all()
        self.assertEqual(1, eigenvalues.count())

        stored_eigenvalue = eigenvalues.first()
        for key, value in data.items():
            self.assertEqual(value, getattr(stored_eigenvalue, key))

        with patch.object(Eigenvalue, "check_consistency") as mocked_check_consistency:
            ev2, created = Eigenvalue.objects.get_or_create(**data)

        self.assertFalse(created)
        mocked_check_consistency.assert_not_called()

        eigenvalues = Eigenvalue.objects.all()
        self.assertEqual(1, eigenvalues.count())
        self.assertEqual(ev, ev2)

    def test_get_or_create_consistency_fail(self):
        """Calls `get_or_create` such that an `ConsistencyError` is triggered.

        Expects `ConsistencyError` is raised an no eigenvalue is created.
        """
        data = {
            "hamiltonian": self.hamiltonian,
            "n_level": self.hamiltonian.n_sites + 1,
            "value": Decimal("0.0"),
            "tag": None,
        }

        with self.assertRaises(ConsistencyError) as context:
            Eigenvalue.objects.get_or_create(**data)

        self.assertIsInstance(context.exception.error, ValueError)

        eigenvalues = Eigenvalue.objects.all()
        self.assertEqual(0, eigenvalues.count())

    def test_get_or_create_from_parameters_1(self):
        """Tests the get or create from parameters method for existing hamiltonian.
        """
        data = {
            "n_level": 0,
            "value": Decimal("0.0"),
            "n_sites": self.hamiltonian.n_sites,
            "spacing": self.hamiltonian.spacing,
            "c": self.hamiltonian.c,
        }
        tree = {"hamiltonian": "Contact"}
        _, created = Eigenvalue.get_or_create_from_parameters(data, tree=tree)

        self.assertTrue(created)

        hamiltonians = Hamiltonian.objects.all()
        self.assertEqual(hamiltonians.count(), 1)

        hamiltonian = hamiltonians.first()
        self.assertEqual(hamiltonian.type, tree["hamiltonian"])
        self.assertEqual(hamiltonian.n_sites, data["n_sites"])
        self.assertEqual(hamiltonian.spacing, data["spacing"])
        self.assertEqual(hamiltonian.c, data["c"])

        eigenvalues = Eigenvalue.objects.all()
        self.assertEqual(eigenvalues.count(), 1)
        eigenvalue = eigenvalues.first()
        self.assertEqual(eigenvalue.hamiltonian, hamiltonian)
        self.assertEqual(eigenvalue.value, data["value"])
        self.assertEqual(eigenvalue.n_level, data["n_level"])

    def test_get_or_create_from_parameters_2(self):
        """Tests the get or create from parameters method for existing hamiltonian.
        """
        data = {
            "n_level": 0,
            "value": Decimal("0.0"),
            "n_sites": 10,
            "spacing": Decimal("0.1"),
            "c": Decimal("-2.0"),
        }
        tree = {"hamiltonian": "Contact"}
        _, created = Eigenvalue.get_or_create_from_parameters(data, tree=tree)

        self.assertTrue(created)

        hamiltonians = Hamiltonian.objects.all()
        self.assertEqual(hamiltonians.count(), 2)

        hamiltonian = hamiltonians.last()
        self.assertEqual(hamiltonian.type, tree["hamiltonian"])
        self.assertEqual(hamiltonian.n_sites, data["n_sites"])
        self.assertEqual(hamiltonian.spacing, data["spacing"])
        self.assertEqual(hamiltonian.c, data["c"])

        eigenvalues = Eigenvalue.objects.all()
        self.assertEqual(eigenvalues.count(), 1)
        eigenvalue = eigenvalues.first()
        self.assertEqual(eigenvalue.hamiltonian, hamiltonian)
        self.assertEqual(eigenvalue.value, data["value"])
        self.assertEqual(eigenvalue.n_level, data["n_level"])

    def test_create_consistency_turned_off(self):
        """Tests wether inserting an eigenvalue entry using `create` works as
        expected when turning off consistency checks.

        Tests:
            1. Save method calls check_consistency with expected arguments
            2. The eigenvalue is properly inserted
        """
        data = {
            "hamiltonian": self.hamiltonian,
            "n_level": 1000,
            "value": Decimal("0.0"),
            "tag": None,
        }

        ev = Eigenvalue(**data)
        ev.run_checks = False
        with patch.object(Eigenvalue, "check_consistency") as mocked_check_consistency:
            ev.save()

        mocked_check_consistency.assert_not_called()

        eigenvalues = Eigenvalue.objects.all()
        self.assertEqual(1, eigenvalues.count())

        stored_eigenvalue = eigenvalues.first()
        for key, value in data.items():
            self.assertEqual(value, getattr(stored_eigenvalue, key))

    def test_get_or_create_from_parameters_fail_atomicness(self):
        """Tests the get or create from parameters method for not existing hamiltonian
        and fail at eigenvalue level.
        """
        data = {
            "n_level": 11,  # causes fail
            "value": Decimal("0.0"),
            "n_sites": 10,
            "spacing": Decimal("0.1"),
            "c": Decimal("-2.0"),
        }
        tree = {"hamiltonian": "Contact"}

        hamiltonians = Hamiltonian.objects.all()
        self.assertEqual(hamiltonians.count(), 1)

        with self.assertRaises(ConsistencyError):
            Eigenvalue.get_or_create_from_parameters(data, tree=tree)

        hamiltonians = Hamiltonian.objects.all()
        self.assertEqual(hamiltonians.count(), 1)

        eigenvalues = Eigenvalue.objects.all()
        self.assertEqual(eigenvalues.count(), 0)
