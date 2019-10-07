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

Since now the table structure was modified, changes need to be migrated
```bash
$ python manage.py makemigrations
Migrations for 'hamiltonian':
  my_project/hamiltonian/migrations/0002_eigenvalue.py
    - Create model Eigenvalue
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, hamiltonian, notifications, sessions
Running migrations:
  Applying hamiltonian.0002_eigenvalue... OK
```

## Updating the run script
