"""A simple script which adds data to the tables
"""
from itertools import product

import numpy as np

from my_project.hamiltonian.models import IsingModel
from my_project.hamiltonian.models import Eigenvalue

RANGES = {"j": np.linspace(0.1, 1.0, 10), "n_sites": np.arange(10, 51, 5)}


def get_hamiltonian(j: float = 1.0, n_sites: int = 10) -> np.ndarray:
    """Implements the nearest neighbor Ising model hamiltonian in one dimension.
    """
    h = np.zeros([n_sites, n_sites], dtype=float)

    for n in range(n_sites):
        h[n, (n + 1) % n_sites] -= j
        h[n, (n - 1) % n_sites] -= j

    return h


def main():
    """Exports eigenvalues of the nearest neighbor Ising model for differnt parameters.

    Before exporting, the database is asked if eigenvalues for given system are already
    present. If so, the computation is skipped.
    """
    for values in product(*RANGES.values()):
        j, n_sites = values

        print(f"Start to compute eigenvalues for j={j} and n_sites={n_sites}.")

        # check if entries have not been computed yet
        ## (entries are unique in j and n_sites, so first is fine)
        compute_entries = True
        ising_entry = IsingModel.objects.filter(j=j, n_sites=n_sites).first()
        if ising_entry:
            print(f"  Found entry in table: {ising_entry}")
            # Check if eigenvalues have been computed before
            eigenvalues = Eigenvalue.objects.filter(matrix=ising_entry)
            if eigenvalues.count() > 0:
                print("  But eigenvalues where already computed")
                compute_entries = False
        else:
            # Because we do not have a table entry yet, we create a Python instance
            ising_entry = IsingModel(j=j, n_sites=n_sites)
            print(f"  Creating table entry for {ising_entry}")
            # And insert it in the database
            ising_entry.save()

        if compute_entries:
            # Compute eigenvalues
            print("  Allocating hamiltonian")
            hamiltonian = get_hamiltonian(j=j, n_sites=n_sites)
            eigs, _ = np.linalg.eigh(hamiltonian)

            # Create database entries
            ## Because we know that the entries do not exist and we will create many
            ## It is good practice to create all python instances first
            print("  Preparing export of eigenvalues")
            eigen_entries = []
            for n_level, value in enumerate(eigs):
                eigen_entries.append(
                    Eigenvalue(matrix=ising_entry, n_level=n_level, value=value)
                )
            ## And connect to the DB only once -- when all Python objects are known
            bulk = Eigenvalue.objects.bulk_create(eigen_entries)
            print(f"  Exported {len(bulk)} entries")

    print("Done")


if __name__ == "__main__":
    main()
