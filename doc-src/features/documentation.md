# Documentation

EspressoDB comes with automatic documentation of all present tables (if not otherwise specified).

To do so, your tables must inherit from the EspressoDB model `Base` class.
EspressoDB will scan your models after existing and editable fields and will generate a webpage for each web-app which summarize the columns.

See also [the documentation API](../api/documentation/index) for more examples
