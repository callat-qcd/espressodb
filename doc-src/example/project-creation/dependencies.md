# Adding tables with relationships


## Updating the models
Next we want to prepare actual computations.
For example, if we are interested in storing eigenvalues, we should create a new table for them in `my_project.hamiltonian.models.py`

```python
...

class Eigenvalue(Base):
    """Model which stores diagonalization information for a given Hamiltonian
    """

    hamiltonian = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        help_text="Matrix for which the eigenvalue has been computed.",
    )
    n_level = models.PositiveIntegerField(
        help_text="The nth eigenvalue extracted in ascending order."
    )
    value = models.FloatField(help_text="The value of the eigenvalue")

    class Meta:
        unique_together = ["hamiltonian", "n_level"]
```

Similar to the `Contact` model, we have a `PositiveIntegerField` which enumerate the eigenvalues and a `value` field, now being a `FloatField`, as we do not use it for unique constraint comparisons.

The `hamiltonian` field, a `ForeignKey` field, points to the `Contact` table.
On the Python side, this would correspond to
```python
e = Eigenvalue.objects.first()
e.hamiltonian # this is a contact hamiltonian class instance
```
Also, a backwards access is provided
```python
h = Contact.objects.first()
h.eigenvalue_set.all()
```
would return of all eigenvalues associated with the hamiltonian.

The `on_delete` specifies what happens if a hamiltonian associated with eigenvalues is deleted.
In particularly, the `models.CASCADE` means if you delete a hamiltonian you also delete all associated eigenvalues.

Since now the table structure was modified, changes need to be migrated
```bash
$ python manage.py makemigrations
Migrations for 'hamiltonian':
  my_project/hamiltonian/migrations/0002_eigenvalue.py
    - Create model Eigenvalue
```
and
```bash
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, hamiltonian, notifications, sessions
Running migrations:
  Applying hamiltonian.0002_eigenvalue... OK
```

## Updating the run script

We now want to extend the script to export eigenvalues in case computations are non-existent or incomplete.
Non-existent is defined by: "We have no eigenvalues" for a given Hamiltonian, incomplete means: "We find less eigenvalues then expected".

This logic is implemented by adjusting the `main` function in `add_data.py`:
```
...

from my_project.hamiltonian.models import Eigenvalue

def main():

    for values in product(*RANGES.values()):
        ...

        compute_entries = True

        eigenvalues = Eigenvalue.objects.filter(hamiltonian=hamiltonian)

        if eigenvalues.count() == n_sites:
            compute_entries = False
        else:
            print("  Eigenvalues incomplete. Deleting old computation.")
            eigenvalues.delete()

        if compute_entries:
            print("  Computing eigenvalues")
            eigs, _ = np.linalg.eigh(hamiltonian.matrix)
            print("  Preparing export of eigenvalues")
            for n_level, value in enumerate(eigs):
                Eigenvalue.objects.create(hamiltonian=hamiltonian, n_level=n_level, value=value)

    print("Done")
```
Running this script will compute all the eigenvalues.

<div class="admonition warning">
<p class="admonition-title">Note</p>
<p>
    EspressoDB automatically stores `user` and `last_modified` information for each entry.
    In some cases it might be desirable to also store code revision information.
    This can be done by specifying the `tag` column.
    See also [the `pre_save` functionality.](../../features/pre-save.md).
</p>
</div>
