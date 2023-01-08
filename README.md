# piplexed - Find outdated packages installed with pipx

[![PyPI - Version](https://img.shields.io/pypi/v/piplexed.svg)](https://pypi.org/project/piplexed)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/piplexed.svg)](https://pypi.org/project/piplexed)

-----

**Table of Contents**

- [Installation](#installation)
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

![piplesed list output](img\piplexed-list.PNG "piplexed list")]

### List outdated packages installed with pipx (no pre or dev release)

```console
piplexed list --outdated
```
Output ignores prelease and dev releases by default.

![piplexed list outdated output](img\piplexed-list-outdated.PNG "piplexed list outdated")]


### List outdated packages installed with pipx


```console
piplexed list --outdated --pre
```
Output includes prerelease and dev releases and highlights them.

![piplexed list outdated pre output](img\piplexed-list-outdated-pre.PNG "piplexed list pre outdated")]
### Why piplexed ?

Dependency managment in the python ecosystem has always been a bit of a pain. For managing dependencies in a virtual environment we have tools like:
- [pip-tools](https://github.com/jazzband/pip-tools)
- [poetry](https://github.com/python-poetry/poetry)

These help to manage project package dependencies and their sub-dependencies.
Some python packages, such as tools like `black`, `mypy`, `flake8`, etc are used in almost every project. To avoid having to install them in every virtual environment, it's helpful to be able to install them once and be able to access them globally from the command line.

This is where a tool like `pipx` comes in handy, essentially any python package that has a console script entry point can be installed in it's own isolated environment but still be run directly from the command line without having to activate any virtual environments.

But the question remains, how do you tell if there is a new version of a package you have installed with `pipx` ??

`pipx` has a `list` command which shows all the packages (excluding dependencies) and their versions installed with pipx, however it doesn't have an `outdated` flag option like `pip`.

```console
(activated-env) $ python -m pip list --outdated
```
There a coupke of issues on pipx's github pages that have been open for a couple of years now
- [#149](https://github.com/pypa/pipx/issues/149)
- [#464](https://github.com/pypa/pipx/issues/464)

Having grown tired of manually checking pypi for new versions and not feeling that currently I have the skill to tackle the above issues, I have rolled my own CLI package to solve this issue.

### How does `piplexed` determine what the latest PyPI version is ?




### Caveats

- Only works for packages that are on [PyPI](https://pypi.org), does not work for local packages or git/url etc.
- Currently no optimisation, so it can be a little slow if you have a lot of pipx installed packages



## License

`piplexed` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
