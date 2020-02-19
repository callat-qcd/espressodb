# EspressoDB

EspressoDB is a Python framework designed to organize (relational) data without losing flexibility.
It's objective is to be intuitive and fast.

More specifically, EspressoDB is build on top of the Object-Relational Mapping web framework [Django](https://docs.djangoproject.com) and adds additional convenience functionalities to easily set up your project.

## What does EspressoDB provide?

EspressoDB provides an easy to use database interface which helps you to make educated decisions fast.

Once you have created your Python project (e.g., `my_project`) with EspressoDB

* you can use it in all your Python apps to query your data. For example,
    ```python
    import numpy as np
    from my_project.hamiltonian.models import Contact as ContactHamiltonian

    # Ask the database for specific entries
    hamiltonian = ContactHamiltonian.objects.filter(n_sites=20).first()

    # Use class methods for an intuitive interface
    ## Print a formatted summary of the table entry
    print(hamiltonian)

    ## Allocate an actual matrix for given entry and use it for computations
    eigs, vecs = np.linalg.eigh(hamiltonian.matrix)
    ```
    Instances of a `models` class are regular classes in Python.
    You can provide additional class methods for convenience.
    Also, they know how to talk to the database, e.g., you can query (read) and update (write) your data to a central database.
* you can generate web-views which summarize your tables and data.
    ![Docpage example](https://raw.githubusercontent.com/callat-qcd/espressodb/master/doc-src/_static/webview-example.png)
    Because the webpages use a Python API as well, this means that you can completely customize views with code you have already developed.
    E.g., you can automate plots and display summaries in your browser.
    If you want to, you can also make your web app public (with different layers of accessibility) and share results with others.


## How to install it?
EspressoDB can be installed via pip
```bash
pip install [--user] espressodb
```

## What's the story behind it?

EspressoDB was developed when we created [LatteDB](https://www.github.com/callat-qcd/lattedb) -- a database for organizing Lattice Quantum Chromodynamics research.
We intended to create a database for several purposes, e.g. to optimize the scheduling of architecture dependent many-node jobs and to help in the eventual analysis process.
For this reason we started to abstract our thinking of how to organize physics objects.

It was the goal to have easily shareable and completely reproducible snapshots of our workflow, while being flexible and not restricting ourselves too much -- in the end science is full of surprises.
The challenges we encountered were
1. How can we program a table structure which can be easily extended in the future?
2. How do we write a database such that users not familiar with the database concept can start using this tool with minimal effort?

The core module of LatteDB, EspressoDB, is trying to address those challenges.

## Who is responsible for it?
* [@cchang5](https://github.com/cchang5)
* [@ckoerber](https://github.com/ckoerber)

## Contributing
Thanks for your interest in contributing! There are many ways to contribute to this project.
[Get started here](CONTRIBUTING.md).


## License

BSD 3-Clause License. See also the [LICENSE](LICENSE.md) file.
