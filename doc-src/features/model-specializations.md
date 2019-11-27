# More complicated tables

This section explains how one can build tables such that they are extendable in the future.
It is presented in the case of [the example project](../example/index).

## In which scenario are they helpful
In science projects it is usually hard if not impossible to plan out each step at the beginning of a project.
Thus it is important to stay flexible enough to incorporate unexpected changes -- which, on first thought, is not along the notions of using relatively fixed tables.

Suppose you are in the scenario where you want to extend the previously coded up `ContactHamiltoninan`.
If it makes sense, you can add new columns and decide how previous entries in the tables, which where inserted without this new columns in mind, add default values.

Sometimes this is not enough -- it would not make sense to adjust existing tables such that all new changes are present.
As an example, you would like to include a new Hamiltonian, e.g., corresponding to Coulomb interactions which are conceptually completely different from the `ContactHamiltoninan`.
But still you are interested in eigenvalue solutions which connection is hard coded to the `ContactHamiltoninan` by the `hamiltonian` foreign key.

A possible solution would be to code up the new `CoulombHamiltoninan` and introduce a new `CoulombEigenvalue` which `hamiltonian` foreign key points to the `CoulombHamiltoninan`.

```python
class Coulomb(Base):
    ...

class  CoulombEigenvalue(Base):
    hamiltonian = models.ForeignKey(Coulomb, on_delete=models.CASCADE)
    ...
```

However, this now means that we have two `Eigenvalue` classes which represent the same thing and their only difference is the hamiltonian they point to
```
Eigenvalue -> Contact
CoulombEigenvalue -> Coulomb
```

A nicer solution would be if the eigenvalue point to a common base class, e.g., a Hamiltonian which is either a `Coulomb` or `Contact` Hamiltonian
```
Eigenvalue -> Hamiltonian <-> Contact
                          <-> Coulomb
```
This way, you will always have one eigenvalue class which generalizes to all ideas of an Hamiltonian class.

## Implementation of common base

<div class="admonition warning">
<p class="admonition-title">Warning</p>
<p>In this section we want to present the general idea for more complex tables.</p>
<p>It is in general difficult to completely reshape existing tables and therefore one should plan ahead!</p>
<p>To test the changes for this project, we recommend starting the database from scratch (e.g., remove the <code>.sqlite</code> file and <code>my_project/hamiltonian/migrations</code> files)</p>
</div>

### The implementation
Django already provides a framework for implementing such common base tables using inheritance.
E.g., the most minimal setup for such a scenario would be

```python
class Hamiltonian(Base):
    pass

class Contact(Hamiltonian):
    n_sites = models.IntegerField()
    spacing = models.DecimalField(max_digits=5, decimal_places=3)
    c = models.DecimalField(max_digits=5, decimal_places=3,)

    class Meta:
        unique_together = ["n_sites", "spacing", "c"]

class Coulomb(Hamiltonian):
    n_sites = models.IntegerField()
    spacing = models.DecimalField(max_digits=5, decimal_places=3)
    v = models.DecimalField( max_digits=5, decimal_places=3)

    class Meta:
        unique_together = ["n_sites", "spacing", "v"]

class Eigenvalue(Base):
    hamiltonian = models.ForeignKey(Hamiltonian, on_delete=models.CASCADE)
    n_level = models.PositiveIntegerField()
    value = models.FloatField()

    class Meta:
        unique_together = ["hamiltonian", "n_level"]
```
The `Eigenvalue` class now points to the `Hamiltonian` table and the `Contact` and `Coulomb` Hamiltonian classes now inherit from `Hamiltonian`.

The new classes can be used as before, e.g.,
```python
h1 = Contact.objects.create(n_sites=10, spacing=0.1, c=-1)
h2 = Coulomb.objects.create(n_sites=10, spacing=0.1, v=20)

e1  = Eigenvalue.objects.create(hamiltonian=h1, n_level=1, value=-363.823)
e2 = Eigenvalue.objects.create(hamiltonian=h2, n_level=1, value=234.567)
```

### Underlaying tables

Different to the base table, the `Hamiltonian` table is not abstract and thus will actually be created.
E.g., these models will create the following tables after migrating

#### `hamiltonian_hamiltonian`

| id | last_modified | tag | userid|
|---|---|---|---|
| 1 | ... | ... | ...|
| 2  ... | ... | ...|
| ... | ... | ... | ...|
| 42 | ... | ... | ...|
| ... | ... | ... | ...|

The `id` column is the primary key to identify a certain entry.
All the other columns come from the EspressoDB `Base` class (which does not have it's own table) to enable EspressoDB's features and have additional meta information.

#### `hamiltonian_contact`

| hamiltonian_ptr_id | n_sites | spacing | c |
|---|---|---|---|
| 1 | 10 | 0.1 | -1 |
| 2 | 15 | 0.1 | -1 |
| ... | ... | ... | ... |

The specialized `hamiltonian_contact` table has no own `id`.
It uses the `id` column of the `hamiltonian_hamiltonian` table using the `hamiltonian_ptr_id`.
The other entries are specific to the actual implementation.

#### `hamiltonian_coulomb`

| hamiltonian_ptr_id | n_sites | spacing | v |
|---|---|---|---|
| 42 | 10 | 0.1 | -02 |
| ... | ... | ... | ... |

Similarly, the `hamiltonian_coulomb` borrows it's primary key from the `hamiltonian_hamiltonian` table and adds information specific to it in it's own table.

Thus, all implementations have a corresponding entry in the base `hamiltonian_hamiltonian` table but specific information in their own table.

#### `hamiltonian_eigenvalue`

| id | last_modified | tag | n_level | value | hamiltonian_id | userid |
|---|---|---|---|---|---|---|
| 1 | ... | ... | 1 | -363.823 | 1 | ... |
| 1 | ... | ... | 2 | -361.803 | 1 | ... |
| ... | ... | ... | ... | ... | ... |

Because the `hamiltonian_eigenvalue` table inherits from `Base`, it comes with the default `Base` columns.
In addition, it now points to the `hamiltonian_id` in the `hamiltonian_hamiltonian` table which corresponds to either a specialized `Coulomb` or `Contact` entry.

### Unique constraints

Because both the `Contact` and `Coulomb` table have information about `n_sites` and `spacing`, it would actually be possible to move these information to the base `Hamiltonian` table.
This is generally possible and might also be good practice depending on the specific situation.
However, in case there are joined unique constraints, it might not always be possible because this constraint is enforced at the table level.

Suppose you want all the `Contact` entries to be unique in `["n_sites", "spacing", "c"]`.
If you place the additional columns `n_sites` and `spacing` from `Contact` to `Hamiltonian` and add an unique constraint in `Hamiltonian` according to `["n_sites", "spacing"]`,

```python
class Hamiltonian(Base):
    n_sites = models.IntegerField()
    spacing = models.DecimalField(max_digits=5, decimal_places=3)

    class Meta:
        unique_together = ["n_sites", "spacing"]

class Contact(Hamiltonian):
    c = models.DecimalField(max_digits=5, decimal_places=3)

    class Meta:
        unique_together = ["hamiltonian_ptr_id", "c"]
```
it is **not** possible to have table entries for same `n_site` and `spacing` but different `c`,

#### `hamiltonian_hamiltonian`

| id | n_sites | spacing | ... |
|---|---|---|---|
| 1 | 10 | 0.1 | ...|
| ... | ... | ... | ...|

#### `hamiltonian_contact`

| hamiltonian_ptr_id | c |
|---|---|
| 1 | -1.0 |
| 1 | -2.0 _(this is not possible)_ |

because each entry in `hamiltonian_contact` creates a new `id` in `hamiltonian_hamiltonian` which is unique constrained in the parameters we want to have present.

In principle one could unique constrain `["id", "n_sites", "spacing"]` in `hamiltonian_hamiltonian`, however unique constraining any combination of columns containing the `id` is equivalent to not constraining at all (because the `id` is supposed to be unique).


### Queries and member access

In case of inheritance, queries and member access changes slightly.
E.g., if one wants to look up the corresponding `Contact` Hamiltonian of eigenvalues, one would have to use the following code
```
h = Eigenvalue.objects.filter(hamiltonian__contact__c=-1.0).first()
```

Or on the python level
```python
e1 = Eigenvalue.objects.first()
h = e1.hamiltonian.contact # potentially none if hamiltonian not of type contact
h.c == -1.0
```
Note that this access might fail if the Hamiltonian is a `Coulomb` Hamiltonian.

To be save against this, EspressoDB provides the `specialization` attribute which identifies the type of the instance by it's primary key, e.g.,
```python
h0 = e1.hamiltonian.specialization
h0 == h
```

Furthermore, to avoid redundancy, EspressoDB provides convenience methods to circumvent the access of the specialization attribute.
E.g., it is possible to use the syntax
```python
e1 = Eigenvalue.objects.first()
h = e1.hamiltonian # no extra access to .contact
h.c == -1.0 # only present if h2 is of type contact, else it is .v
```

<div class="admonition note">
<p class="admonition-title">Note</p>
<p>
    Note that <code>h</code> is still an instance of <code>Hamiltonian</code>, it just loads in all the members of <code>Contact</code>.
    When you change the members belonging to <code>Contact</code>, and call <code>save</code>, also the corresponding save of <code>Contact</code> is called.
</p>
</div>
