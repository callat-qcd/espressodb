# Pre-save functionality

## TL;DR

EspressoDB's `Base` class implements the `.pre_save()` method which is run before `.check_consistency()` and before inserting data into the database.
This functionality can be used to insert default values for columns that depend on runtime information.

<div class="admonition warning">
<p class="admonition-title">Note</p>
<p>
    Similar to the <code>.check_consistency()</code> method, <code>.pre_save()</code> is not executed on bulk creation or update events.
</p>
</div>

## Implementing a code version storage

The most prominent use case for employing a `pre_save` check is to store code revision information.
For example

```python
def get_code_revision() -> str:
    """Extracts version of code which generates data by ...
    """
    return ...

BAD_REVISIONS = ["v0.7.6a", "v99.99.1b"]

class Data(Base):
    value = models.FloatField(help_text="Important number")
    tag = models.CharField(max_length=200, help_text="Code revision")

    def pre_save(self):
        """Populates the `tag` column with the code revision.

        This method is run before updating the database.
        """
        self.tag = get_code_revision()

    def check_consistency(self):
        """Checks if code used for generating data is not part of a bad revision.

        This is run after `pre_save` but before inserting in the database.
        """
        if self.tag in BAD_REVISIONS:
            raise RuntimeError(
                f"You should not use revision '{self.tag}' for exporting data."
            )
```

If a user now runs
```python
Data(value=6.123).save()
```
the `Data` class will fill the `tag` field with `get_code_revision()` and only store entries if they are not part of `BAD_REVISIONS`.

Similar to `.check_consistency()`, `.pre_save()` can be disabled for the whole class or for a single instance by the `run_pre_save` attribute:
```bash
Data.run_pre_save = False # for all future instances
# or
instance = Data(value=1.23)
instance.run_pre_save = False # for only this instance
```
