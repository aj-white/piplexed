# Piplexed - Find outdated packages installed with pipx

[![PyPI - Version](https://img.shields.io/pypi/v/piplexed.svg)](https://pypi.org/project/piplexed)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/piplexed)](https://pypi.org/project/piplexed)

**Documentation**: [https://aj-white.github.io/piplexed/](https://aj-white.github.io/piplexed/)

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [Why piplexed ?](#why-piplexed)
- [Caveats](#caveats)
- [License](#license)

## Overview: What is piplexed ?

**Piplexed** is a command line tool to identify outdated python packages, installed from [PyPI](https://pypi.org/), via [pipx](https://pypa.github.io/pipx/). It displays it's output as a nice [rich](https://github.com/Textualize/rich) printed tree.


## Installation

**Piplexed** is designed to be installed globally via **pipx**.

To install **piplexed**:

```console
pipx install piplexed
```

Alternatively you can run it wihtout installation, supplying the required arguments shown below

```console
pipx run -- piplexed <ARGS>
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

The name **piplexed** is a play on words, it contains the letters for pipx and I was also mildly perplexed trying to find a simpler way to identify outdated pipx installed packages, only to discover it didn't exist. Put the two together and well.... you get the idea (naming things is hard after all!).
For a longer answer see the [documentation](https://aj-white.github.io/piplexed/Why-piplexed/).


## Caveats

**Piplexed** is a project that I built for my workflow, but it may not work for everyone.

It is only intended to work for packages that are installed from [PyPI](https://pypi.org), so will not work for local packages or git/url etc.

## License

**Piplexed** is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
