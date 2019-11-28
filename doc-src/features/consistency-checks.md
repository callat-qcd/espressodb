# Consistency checks

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

## 
