# Contributing to EspressoDB

Thank you for considering contributing to EspressoDB.
On this page, we line out of how to best help out.
And of course, please make sure you are welcoming and friendly (see also the [Python community code of conduct](https://www.python.org/psf/conduct/)).

## Guiding principles

EspressoDB is an open-source project which intends to simplify others (programming) live.
At best, an EspressoDB user should not worry about details behind the scenes; but if required, they should know what to do to adjust their EspressoDB project to their needs.
For this reason, it is one of our guiding principles to stay close to [Django](https://www.djangoproject.com).
This allows utilizing existing functionality, resources and staying compatible as much as possible.

Because Django comes with a [vast amount of documentation](https://docs.djangoproject.com/en/dev/) and has [rich community support](https://stackoverflow.com/questions/tagged/django),
it might be that the questions you have concerning EspressoDB are already explained in the resources on Django.
If you think that this is not the case, feel free to reach out.

## What we are looking for

EspressoDB is currently used in a few projects specific to our community.
To extend its usability, providing feedback on how you use EspressoDB and how it could simplify your life are valuable to us.
Whether it concerns the documentation or the software itself, if you believe you have ideas on how to improve EspressoDB, please reach out.

## Community: questions & discussions

If you have questions, feel unsure about filing an issue, or rather want to discuss your concerns first, feel free to contact us on [https://groups.google.com/forum/#!forum/espressodb](https://groups.google.com/forum/#!forum/espressodb).

## Filing issues

If you find a potential bug, do not hesitate to contact us and file an issue---we will try to address it as soon as possible.
But also if you feel you have an idea for potential improvement, we welcome issues on feature requests and enhancements.

#### Filing Bugs

When filing a bug report, please let us know:

1. What is your Python, Django and EspressoDB version?
2. What did you do?
3. What did you expect to see?
4. What did you see instead?

## Your first contribution

We do appreciate help in form of pull requests ---just take a look at open issues and try identifying a problem you might be able to help out with.
Before you submit pull requests, please make sure the tests work.

### Tests

To run all tests you have to install the development requirements on top of EspressoDB
```bash
pip install -r requirements-dev.txt
```
Because EspressoDB is used to create other projects, the tests should check whether features of EspressoDB work and also new projects can be initiated as expected.
For this reason, we use a Makefile on top of the regular testing framework.
You can run the tests with
```bash
make test
```

### Preferred style of code

We try to follow [PEP8](https://www.python.org/dev/peps/pep-0008/) as much as useful (see also [Pylint](https://www.pylint.org)).
In this context, we also appreciate formatting along the lines of [black---the uncompromising Python code formatter](https://github.com/psf/black).

### Versioning

EspressoDB follows [Semantic Versioning 2.0.0](https://semver.org) (`MAJOR.MINOR.PATCH`).
Branches start with a `v`, e.g., `v1.1.0` and once merged into master will obtain the previous branch name as a tag.
