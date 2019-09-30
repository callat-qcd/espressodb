"""Models of my_app
"""
from django.db import models
from espressodb.base.models import Base


class SpinHamiltonian(Base):
    """The root table for SpinHamiltonian's.

    This table does not store any infomration about the Hamiltonian itself
    """

    @property
    def mu(self) -> float:  # pylint: disable = C0103
        """Magnetic moment of the degrees of freedom.
        """
        return 0.5


class IsingModel(SpinHamiltonian):
    r"""Model which stores implementation of uniform Ising model without external field.

    The Hamiltonian is given by
    $$
        H = -J\sum_{\text{NN}} \sigma_i \sigma_j
    $$
    where NN specifies the set of nearest neighbors.
    """

    j = models.DecimalField(
        verbose_name="Interaction",
        max_digits=5,
        decimal_places=3,
        help_text="Interaction parameter of th the Ising Model."
        " Implements uniform nearest neighbor interactions.",
    )
    n_sites = models.IntegerField(
        verbose_name="Number of sites",
        help_text="Number of sites in one spatial dimension",
    )

    class Meta:  # pylint: disable=C0111, R0903
        unique_together = ["j", "n_sites"]


class ExteranlFieldIsingModel(SpinHamiltonian):
    r"""Model which stores implementation of uniform Ising model with external field.

    The Hamiltonian is given by
    $$
        H = -J\sum_{\text{NN}} \sigma_i \sigma_j - \mu h \sum_j \sigma_j
    $$
    where NN specifies the set of nearest neighbors.
    """

    j = models.DecimalField(
        verbose_name="Interaction",
        max_digits=5,
        decimal_places=3,
        help_text="Interaction parameter of th the Ising Model."
        " Implements uniform nearest neighbor interactions.",
    )
    h = models.DecimalField(
        verbose_name="External magnetic field",
        max_digits=5,
        decimal_places=3,
        help_text="Implements uniform magnetic field:"
        " Implements uniform nearest neighbor interactions.",
    )
    n_sites = models.IntegerField(
        verbose_name="Number of sites",
        help_text="Number of sites in one spatial dimension",
    )

    class Meta:  # pylint: disable=C0111, R0903
        unique_together = ["j", "h", "n_sites"]


class Eigenvalue(Base):
    """Model which stores diagonalization information for a given SpinHamiltonian
    """

    matrix = models.ForeignKey(
        SpinHamiltonian,
        on_delete=models.CASCADE,
        help_text="Matrix for which the eigenvalue has been computed.",
    )
    n_level = models.PositiveIntegerField(
        help_text="The nth eigenvalue extracted in ascending order."
    )
    value = models.FloatField(help_text="The value of the eigenvalue")

    class Meta:  # pylint: disable=C0111, R0903
        unique_together = ["matrix", "n_level"]
