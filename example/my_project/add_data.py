"""A simple script which adds data to the tables
"""
from itertools import product

import numpy as np

from espressodb.notifications import get_notifier

from my_project.hamiltonian.models import Contact as ContactHamiltonian
from my_project.hamiltonian.models import Eigenvalue


RANGES = {
    "spacing": np.linspace(0.1, 1.0, 10),
    "n_sites": np.arange(10, 51, 5),
    "c": [-1],
}

NOTIFIER = get_notifier(tag="add_data")


def main():
    """Exports eigenvalues of the nearest neighbor Ising model for differnt parameters.

    Before exporting, the database is asked if eigenvalues for given system are already
    present. If so, the computation is skipped.
    """
    for values in product(*RANGES.values()):
        spacing, n_sites, c = values

        print(
            "Start to compute eigenvalues for"
            f" spacing={spacing}, n_sites={n_sites} and c={c}."
        )

        # check if entries have not been computed yet
        ## (entries are unique in j and n_sites, so first is fine)
        compute_entries = True
        hamiltonian = ContactHamiltonian.objects.filter(
            n_sites=n_sites, spacing=spacing, c=c
        ).first()
        if hamiltonian:
            print(f"  Found entry in table: {hamiltonian}")
            # Check if eigenvalues have been computed before
            eigenvalues = Eigenvalue.objects.filter(hamiltonian=hamiltonian)
            if eigenvalues.count() == n_sites:
                print("  But eigenvalues where already computed")
                compute_entries = False
            else:
                print("  Eigenvalues incomplete. Deleting old computation.")
                NOTIFIER.debug(
                    f"Deleted {eigenvalues.count()} entries for {hamiltonian}."
                )
                eigenvalues.delete()
        else:
            # Because we do not have a table entry yet, we create a Python instance
            hamiltonian = ContactHamiltonian(n_sites=n_sites, spacing=spacing, c=c)
            print(f"  Creating table entry for {hamiltonian}")
            # And insert it in the database
            hamiltonian.save()

        if compute_entries:
            # Compute eigenvalues
            print("  Computing eigenvalues of hamiltonian")
            eigs, _ = np.linalg.eigh(hamiltonian.matrix)

            # Create database entries
            ## Because we know that the entries do not exist and we will create many
            ## It is good practice to create all python instances first
            print("  Preparing export of eigenvalues")
            eigen_entries = []
            for n_level, value in enumerate(eigs):
                eigen_entries.append(
                    Eigenvalue(hamiltonian=hamiltonian, n_level=n_level, value=value)
                )
            ## And connect to the DB only once -- when all Python objects are known
            bulk = Eigenvalue.objects.bulk_create(eigen_entries)
            print(f"  Exported {len(bulk)} entries")
            NOTIFIER.info(f"Exported {len(bulk)} entries for {hamiltonian}.")

    print("Done")


if __name__ == "__main__":
    main()
