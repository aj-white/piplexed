# How piplexed works

Below is a brief outline of the strategies employed to make piplexed work.

## How does piplexed find pipx local virtual environments ?

**Piplexed** uses the same paths and/or environment variables that **pipx** uses to determine the environment locations.


## How does piplexed find the version of each pipx installed package ?

When **pipx** installs a package it creates a pipx_metadata.json file in the venv, which contains among other things, the installed package name, version and the python version in the venv.

**Piplexed** finds and parses the pipx_metadata.json file.

## How does piplexed determine what the latest PyPI version is ?

It turns out that determining the *latest* PyPI version of a package is a surprisingly hard thing to do consistently and reliably.
There are 2 APIs for PyPI the json and simple API, with the [simple API](https://warehouse.pypa.io/api-reference/json.html) now being recommended for getting release information.

There is a python wrapper package for the simple api [pypi-simple](https://github.com/jwodder/pypi-simple) that returns a project pagre for each package containing it's version history. However there is no guarenteed order to the release versions.

**Piplexed** uses the simple API for PyPI (via the pypi-simple package), which provides an HTML (or JSON) page that lists all versions of package files (sdists and wheels) that have been uploaded.
Because wheels are often platform specific, there is no guarantee that a suitable wheel distribution is available. **Piplexed** avoids the complications of obtating platform details and python versions and just looks at the *sdist* versions.

**Piplexed** employs the strategy recommended in [PEP 700](https://peps.python.org/pep-0700/) to get the *latest* version, which utilises the [packaging](https://github.com/pypa/packaging) package to parse version numbers.

!!! note
    Most of this info was gleaned from looking at and researching [Bernát Gábor's](https://github.com/gaborbernat) package [pypi-changes](https://github.com/gaborbernat/pypi_changes), which also has heavily influenced this project.