"""Models of hamiltonian
"""
from django.db import models

import numpy as np

from espressodb.base.models import Base


class Hamiltonian(Base):
    """The root table for Hamiltonians.

    This table does not store any information (columns) about the Hamiltonian itself.
    """

    @property
    def mass(self) -> float:  # pylint: disable = C0103
        """Returns the mass of a particle.

        This mass will always be the same and thus it is not a table column.
        """
        return 0.5

    def get_kinetic_matrix(self, n_sites: int, spacing: float) -> np.ndarray:
        """Returns the matrix corresponding to the kinetic part of the Hamiltonian.

        Implements a one-step Laplacian in one dimension.
        """
        matrix = np.zeros([n_sites, n_sites], dtype=float)

        fact = 1 / 2 / self.mass / spacing ** 2

        for n in range(n_sites):
            matrix[n, n] += -2 * fact
            matrix[n, (n + 1) % n_sites] += fact
            matrix[n, (n - 1) % n_sites] += fact

        return matrix


class Contact(Hamiltonian):
    r"""Implementation of an 1D contact interaction Hamiltonian in coordinate space.

    The Hamiltonian is given by
    $$
        H = \frac{1}{2 m} p^2 + c \delta(r - r)
    $$
    where \( p^2 \) is the Laplace operator.

    The basis is a lattice with constant lattice spacing and peridic boundary conditions.
    """

    n_sites = models.IntegerField(
        verbose_name="Number of sites",
        help_text="Number of sites in one spatial dimension",
    )
    spacing = models.DecimalField(
        verbose_name="lattice spacing",
        max_digits=5,
        decimal_places=3,
        help_text="The lattice spacing between sites",
    )
    c = models.DecimalField(
        verbose_name="Interaction",
        max_digits=5,
        decimal_places=3,
        help_text="Interaction parameter of th the Hamiltonian."
        " Implements a contact interaction.",
    )

    class Meta:  # pylint: disable=C0111, R0903
        unique_together = ["n_sites", "spacing", "c"]

    @property
    def matrix(self) -> np.ndarray:
        """Returns the matrix corresponding to the Hamiltonian
        """
        spacing = float(self.spacing)
        matrix = self.get_kinetic_matrix(self.n_sites, spacing)

        matrix[0, 0] += float(self.c) / spacing

        return matrix


class Coulomb(Hamiltonian):
    r"""Implementation of an 1/r Coulomb interaction Hamiltonian in coordinate space.

    The Hamiltonian is given by
    $$
        H = \frac{1}{2 m} p^2 + \frac{v}{r}
    $$
    where \( p^2 \) is the Laplace operator.

    The basis is a lattice with constant lattice spacing \(\epsilon\) and peridic
    boundary conditions.
    The \(r = 0 \) component of the interaction is set to \( \frac{v}{\epsilon} \)
    """

    n_sites = models.IntegerField(
        verbose_name="Number of sites",
        help_text="Number of sites in one spatial dimension",
    )
    spacing = models.DecimalField(
        verbose_name="lattice spacing",
        max_digits=5,
        decimal_places=3,
        help_text="The lattice spacing between sites",
    )
    v = models.DecimalField(
        verbose_name="Interaction",
        max_digits=5,
        decimal_places=3,
        help_text="Interaction parameter of th the Hamiltonian."
        " Implements an `1 / r` interaction.",
    )

    class Meta:  # pylint: disable=C0111, R0903
        unique_together = ["n_sites", "spacing", "v"]

    @property
    def matrix(self) -> np.ndarray:
        """Returns the matrix corresponding to the Hamiltonian
        """
        spacing = float(self.spacing)
        matrix = self.get_kinetic_matrix(self.n_sites, spacing)

        for n in range(self.n_sites):
            matrix[n, n] += self.v / (max(1, n) * spacing)

        return matrix


class Eigenvalue(Base):
    """Model which stores diagonalization information for a given Hamiltonian
    """

    hamiltonian = models.ForeignKey(
        Hamiltonian,
        on_delete=models.CASCADE,
        help_text="Matrix for which the eigenvalue has been computed.",
    )
    n_level = models.PositiveIntegerField(
        help_text="The nth eigenvalue extracted in ascending order."
    )
    value = models.FloatField(help_text="The value of the eigenvalue")

    class Meta:  # pylint: disable=C0111, R0903
        unique_together = ["hamiltonian", "n_level"]

    def check_consistency(self):
        """Checks if the n_level entry does not exceed the dimension of the hamiltonian.
        """
        if self.n_level > self.hamiltonian.n_sites:  # pylint: disable=E1101
            raise ValueError("Eigenstate index larger than matrix allows.")
