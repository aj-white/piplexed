# How piplexed works

Below is a brief outline of the strategies employed to make piplexed work.

### How does piplexed find pipx local virtual environments ?

`piplexed` uses the same method as `pipx`.
Pipx contains a whole list of constants that define where pipx bin and venv directories should be in a nice cross-platform way. This has been blatantly stolen and used in piplexed.

### How does piplexed find the version of each pipx installed package ?

When `pipx` installs a package it creates a pipx_metadata.json file in the venv, which contains among other things, the installed package name, version and the python version in the venv.

`piplexed` finds and parses the pipx_metadata.json file.

### How does piplexed determine what the latest PyPI version is ?

It turns out that determined the *latest* PyPI version of a package is a surprisingly hard thing to do consistently and reliably.
There appears to be 2 APIs for PyPI the json and simple API, with the [simple API](https://warehouse.pypa.io/api-reference/json.html) now being recommended.

However version order isn't guaranteed in the simple API and there are items that are included in the JSON API that aren't in the simple API.

That being said there is a nice wrapper package for the simple api [pypi-simple](https://github.com/jwodder/pypi-simple) and version order and be sorted.

!!! note
    Most of this info was gleaned from looking at and researching [Bernát Gábor's](https://github.com/gaborbernat) package [pypi-changes](https://github.com/gaborbernat/pypi_changes), which also has heavily influenced this project.

`piplexed` uses the simple API for PyPI (via the pypi-simple package), which provides an HTML page that lists all versions of package files (sdists and wheels) that have been uploaded, starting with the oldest. `piplexed` looks at all the sdists in this list (on the assumption that not all packages have wheels or there may not be the necessary platform specific wheels available), and orders them by version, using the very helpful [packaging](https://github.com/pypa/packaging) package.