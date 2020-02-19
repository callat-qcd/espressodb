# Providing short cuts with class methods

Because the tables are implemented by Python classes, you can provide additional functionality.
E.g., by default, EspressoDB's `Base` class provides a descriptive `__str__` method.

Since we want to eventually compute eigenvalues of the Hamiltonian, we want to provide an API to compute a matrix representation of the Hamiltonian.
For example, we can add the following methods to `Contact` in `my_project/hamiltonian/models.py`
```python
import numpy as np

from django.db import models
from espressodb.base.models import Base

class Contact(Base):

    ...

    @property
    def mass(self) -> float:
        return 0.5

    @property
    def matrix(self) -> np.ndarray:
        """Returns the matrix corresponding to the Hamiltonian
        """
        spacing = float(self.spacing)
        matrix = np.zeros([self.n_sites, self.n_sites], dtype=float)

        fact = 1 / 2 / self.mass / spacing ** 2

        # Derivative with periodic boundary conditions
        for n in range(self.n_sites):
            matrix[n, n] += -2 * fact
            matrix[n, (n + 1) % self.n_sites] += fact
            matrix[n, (n - 1) % self.n_sites] += fact

        matrix[0, 0] += float(self.c) / spacing

        return matrix
```
Since we always expect to have the same mass, this mass is not a column but a instance property.

Also note that the `spacing` and `c` column values are cast to a float because they were stored as a `DecimalField`.

To test if it works, start a Python shell (by default, Django will use IPython or bpython if either is installed)
```bash
python manage.py shell
```
and test run following code
```python
[1] from my_project.hamiltonian.models import Contact

[2] h = Contact.objects.first()

[3] h.matrix # this is a numpy array
```

<div class="admonition note">
<p class="admonition-title">Note</p>
<p>
    Note that since we only have modified the Python model for the table but not the actual table (e.g., columns), we do not have to migrate changes.
</p>
</div>
