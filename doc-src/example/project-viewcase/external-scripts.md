# Using your project in external modules

There are two ways to use your project in an external module or script

1. Place your external script in the project root directory
2. Install your module

## Installing your module

On project creation, EspressoDB also creates a `setup.py` file in the project root directory.

After [adjusting this file to your needs](https://docs.python.org/3.7/distutils/setupscript.html), you can run
```
python -m pip install [--user] [-e] .
```
This will place `my_project` in your Python path.
The `[-e]` options symlinks the install against this folder and can be useful incase you want to continue updating this module, e.g., for development purposes.
You can also run this in a virtual environment.

## Using tables

Tables or models on the Python side are classes which can be adjusted to your means.
Each row in the table can be loaded into a Python class instance.
Each column in the table will be an attribute of the instance.
You can thus filter the database to extract the class you where interested in, adjust its attributes and push it back to the database.
For example
```
from my_project.hamiltonian.models import Contact as ContactHamiltonian

...

# Search all the table entries for this value and give me the first match
hamiltonian = ContactHamiltonian.objects.filter(
    n_sites=10, spacing=0,1, c=-1
).first()

# Adjust the attribute
hamiltonian.c = -2

# And push back the modifications to the table
hamiltonian.save()
```
The results of this action will thus also be visible from the web view.

## The `add_data.py` script

The example project comes with a script `add_data.py`.
This script defines a range of computations for which eigenvalues of the contact hamiltonian will be computed.

It checks if for a given hamiltonian, the eigenvalues are already present.
If for a specific hamiltonian, you have less eigenvalues then expected, it assumes that the computation failed,
deletes existing eigenvalues from the database and recomputes them.
It also logs creation and deletion events using the `espressodb.notifications` module.
After you have run the script, you can revisit the homepage and check the status or notifications page.
