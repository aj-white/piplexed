# piplexed - Find outdated packages installed with pipx

[![PyPI - Version](https://img.shields.io/pypi/v/piplexed.svg)](https://pypi.org/project/piplexed)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/piplexed.svg)](https://pypi.org/project/piplexed)

-----

⚠ ⚠    STILL IN DEVELOPMENT - WORKING ON DOCS AND ADDING TESTS    ⚠ ⚠

once complete a version will be uploaded to PyPI

---
**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [Why piplexed ?](#why-piplexed)
- [Caveats](#caveats)
- [License](#license)

## Overview: What is piplexed ?

Piplexed is a command line tool to identify outdated python packages, installed from [PyPI](https://pypi.org/), via [pipx](https://pypa.github.io/pipx/). It displays it's output as a nice [rich](https://github.com/Textualize/rich) printed tree.


## Installation

Piplexed is designed to be installed globally via `pipx`.

To install `piplexed` with `pipx`

```console
pipx install piplexed
```

## Usage

### List packages installed with pipx


```console
piplexed list
```
Outputs similar information to `pipx list`, albeit minus the names of the binaries, in a nice rich tree format.

<p>
<img src="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list.PNG" width=300/>
</p>

### List outdated packages installed with pipx (no pre or dev release)

```console
piplexed list --outdated
```
Output ignores prelease and dev releases by default.

<p>
<img src="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list-outdated.PNG" width=300/>
</p>


### List outdated packages installed with pipx


```console
piplexed list --outdated --pre
```
Output includes prerelease and dev releases and highlights them.

<p>
<img src="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list-outdated-pre.PNG" width=300/>
</p>

## Why piplexed

The name `piplexed` is a play on words, it contains the letters for pipx and I was also mildly perplexed trying to find a simpler way to identify outdated pipx installed packages, only to discover it didn't exist. Put the two together and well.... you get the idea (naming things is hard after all!).
For a longer answer see the documentation.


## Caveats

- Only works for packages that are on [PyPI](https://pypi.org), does not work for local packages or git/url etc.
- Currently no optimisation, so it can be a little slow if you have a lot of pipx installed packages.
- Has only been tested on windows 10, as `piplexed` uses that same method of venv discovery as `pipx` it should also work on macOS and linux but there are no guarantees.

## License

`piplexed` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
