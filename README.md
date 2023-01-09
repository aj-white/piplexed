# piplexed - Find outdated packages installed with pipx

[![PyPI - Version](https://img.shields.io/pypi/v/piplexed.svg)](https://pypi.org/project/piplexed)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/piplexed.svg)](https://pypi.org/project/piplexed)

-----

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [Why piplexed ?](#why-piplexed)
- [Caveats](#caveats)
- [License](#license)

## Overview: What is piplexed ?

`piplexed` is a command line tool to help you easily identify packages that have been installed with [pipx](https://github.com/pypa/pipx) that have a newer release on PyPI. 

It attempts to replicate the functionality of the `pip list --outdated` command, but only for pipx installed packages and not their dependencies.


## Installation

Piplexed is designed to be installed globally via `pipx`.

To install `piplexed` with `pipx`

```console
pipx install piplexed
```

Alternatively you can run it with `pipx` wihtout installing it.

```console
pipx run piplexed
```

## Usage


### List packages installed with pipx


```console
piplexed list
```
Outputs similar information to `pipx list`, albeit minus the names of the binaries, in a nice rich tree format.

<p>
<img src="https://github.com/aj-white/piplexed/raw/main/img/piplexed-list.PNG" width=300/>
</p>

### List outdated packages installed with pipx (no pre or dev release)

```console
piplexed list --outdated
```
Output ignores prelease and dev releases by default.

<p>
<img src="https://github.com/aj-white/piplexed/raw/main/img/piplexed-list-outdated.PNG" width=300/>
</p>


### List outdated packages installed with pipx


```console
piplexed list --outdated --pre
```
Output includes prerelease and dev releases and highlights them.

<p>
<img src="https://github.com/aj-white/piplexed/raw/main/img/piplexed-list-outdated-pre.PNG" width=300/>
</p>

## Why piplexed

Dependency managment in the python ecosystem has always been a bit of a pain. It is usually recommended to create a virtual environment for each new project.

However, some python packages, such as tools like `black`, `mypy`, `flake8`, etc are used in almost every project. To avoid having to install them in every virtual environment, taking up disk space and installation time, it would be helpful to install them once and be able to access them globally from the command line.

This is where a tool like `pipx` comes in handy, essentially any python package that has a console script entry point can be installed in it's own isolated environment but still be run directly from the command line without requiring any virtual environments activation.

This is obviously very useful, but as time progresses newer package versions are released and there always comes a time in most projects where updating a dependency to a later version is required. 

To find out if newer versions are available `pip list --outdated` can be run within a virtual environment. This will show any dependency that has a newer version on PyPI, including sub-dependnecies.

To faciliate the managemnt of dependencies and sub-dependencies in a virtual environment there are tools like:
- [pip-tools](https://github.com/jazzband/pip-tools)
- [poetry](https://github.com/python-poetry/poetry)

These all work on a per environment basis, however in `pipx` each of the packages is in it's own virtual environment so these type of tools don't help, *so what can be done?*

`pipx` has a `list` command which shows all the packages installed with pipx (excluding dependencies) and their versions. however it doesn't have an `outdated` option like `pip`.

There are a couple of issues on pipx's github page that have been open for a couple of years now looking at this feature:
- [#149](https://github.com/pypa/pipx/issues/149)
- [#464](https://github.com/pypa/pipx/issues/464)

Having grown tired of manually checking pypi for new versions I've hacked together my own solution.
You may ask why not fix one of the above issues ? That's a perfectly valid question. The truth is I currently don't feel like I have the skills to provide a robust enough solution that would work across multiple OS to satisfy the requirements of a package as widely used as `pipx`

### How does `piplexed` find pipx local virtual environments ?

`piplexed` uses the same method as `pipx`

### How does `piplexed` find pipx local virtual environments ?

When `pipx` installs a package it creates a pipx_metadata.json file in the venv, which contains amoung other things, the installed package name, version and the python version in the venv. `piplexed` finds and parses the pipx_metadata.json file.

### How does `piplexed` determine what the latest PyPI version is ?

`piplexed` uses the simple API for PyPI (via the PySimple package), provides an HTML page that lists all versions of package files (sdists and wheels) that hav ebeen uploaded, starting with the oldest. `piplexed` looks at all the sdists in this list (on the assumption that not all packages have wheels or there may not be the necessary platform specific wheels available), starting with the last.


### Caveats

- Only works for packages that are on [PyPI](https://pypi.org), does not work for local packages or git/url etc.
- Currently no optimisation, so it can be a little slow if you have a lot of pipx installed packages.
- Has only been tested on windows 10, as `piplexed` uses that same method of venv discovery as `pipx` it should also work on macOS and linux but there are no guarantees.



## License

`piplexed` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
