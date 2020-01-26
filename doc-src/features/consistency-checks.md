# Consistency checks

## TL;DR

EspressoDB's `Base` class implements two methods which run tests before inserting data into the database.
Before the database is touched (and unless specified differently)

1. the the instance's `check_consistency` method is called whenever a model is `save`d, `create`d or `update`d and
2. the instance's `check_m2m_consistency` is called whenever a many-to-many column is changed.

On default, these methods are empty; overwriting the methods allows to run tests.
For example,

```python
class A(Base):
    i = models.IntegerField()

    def check_consistency(self):
        if i < 0:
            raise ValueError("`i` too small...")

A.objects.create(i=-2)  # will fail
```

<div class="admonition warning">
<p class="admonition-title">Note</p>
<p>
    These checks are not executed on bulk creation or update events.
</p>
</div>


## The need for checks

For large scales projects it is important to rely on consistent data.
Compared to simple file based solutions, SQL frameworks already provide powerful integrity cross checks in the form type checks and tracking of relations between different tables.
Particularly for scientific projects, it is important for data to fulfill further constraints, like quantitative comparisons between different columns.

Depending on the complexity of consistency checks, a general SQL framework might not be sufficient and one can only leverage the ORM to run these cross checks.
Picture the following scenario: One wants to store the location, filename, type and size of files in a table.
If for a given type and filename, the file size is unexceptionally low, this might suggests that the file is broken.
Once the table checks such cases before insertion and only inserts valid entries (or turn on a warning flag), one can increase consistency of records.
Having sufficient consistency checks before insertion allows automating the data population without endangering consistency.

The basic idea of such checks is already present in Django's `ModelForm`s.
The difference to EspressoDB is that the user of EspressoDB is simultaneously a developer programmatically interacting with the database.
Thus EspressoDB extended the checks to programmatic insertions.

## The basic idea

The checks are captured by Django's signals.
E.g., the `check_consistency` method listens to each `pre_save` signal and `check_m2m_consistency` listens to `m2m_changed`.
These tests are intended to work before an object was created.
Thus you should not rely on the `pk` or `id` column of the to be tested instance when writing checks.

## Disable checks

Each class comes with `run_checks` flag.
Set this flag to `False` to disable checks.
This can be either done on an instance or on the class (which will stop/start checks on all instances)
E.g., the below snippet will fail
```python
a = A(i=-2)  # no check_consistency call yet
a.save() # will fail
```
while the following snippet turns off checks and will succeed.
```
a.run_checks = False # or `A.run_checks` = False to set it for all future instances
a.save()  # will run
```

## Raised exceptions

The checks are wrapped with an exception block which catches the actual exception and raises an informative `ConsistencyError`.
This error carries information about the original exception and has a format message presenting information present at the test.
For example
```python
a = A(i=-2)
```
raises
```
ConsistencyError: Consistency error when checking <class 'A'>.
ValueError:
	`i` too small...
Data used for check:
	* tag: None
	* i: -2
```

## Many-to-many checks

The general idea for many to many checks is analogue to the single instance checks.
Different to this idea is that the many to many instances need to be created before storing their relation.
Thus, this test is rather a test on association between different instances then an actual before creation test of individual instances (it checks consistency before insertion in the through table).
E.g.,
```python
class B(Base):
    a_set = models.ManyToManyField(A)

a = A.objects.first()

b = B.objects.create()  # runs check_consistency on b
b.a_set.add(a) # runs check_m2m_consistency on b with a
```

By default, `check_m2m_consistency` is empty.
To implement custom checks, one has to override the signature.
E.g.,
```python
class B(Base):
    a_set = models.ManyToManyField(A)

    def check_m2m_consistency(self, instances_to_add, column):
        if column == "a_set":
            for a in instances_to_add:
                if a.i > 2:
                    raise ValueError("A instance has too large i...")

b = B.objects.create()  # runs check_consistency on b
a3 = A.objects.create(i=3) # runs check_consistency on a3
b.a_set.add(a3)  # runs check_m2m_consistency on b with a3 and will fail
```

Because on default, `ManyToMany` fields are symmetric, it is in principle possible to run
```python
a3.b_set.add(b)
```
EspressoDB implements consistency checks such that the `check_m2m_consistency` is always called on the instance that has implemented the `ManyToManyField`.
For example, the above call would result in
```python
b.check_consistency(<QuerySet [<A: A[Base](i=3)>]>, column="a_set")
```

Calling `add` with multiple instances results in
```python
> b.a_set.add(a1, a2)

b.check_consistency(<QuerySet [<A: A[Base](i=1)>, <A: A[Base](i=2)>]>, column="a_set")
```
and in the reverse case
```python
> a3.b_set.add(b1, b2)

b1.check_consistency(<QuerySet [<A: A[Base](i=3)>]>, column="a_set")
b2.check_consistency(<QuerySet [<A: A[Base](i=3)>]>, column="a_set")
```
