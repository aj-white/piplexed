<div align="center">

# Piplexed

### Find outdated packages installed with pipx or uv

[![PyPI - Version](https://img.shields.io/pypi/v/piplexed.svg)](https://pypi.org/project/piplexed)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/piplexed)](https://pypi.org/project/piplexed)

**Piplexed** is a command line tool to identify outdated python packages, installed from [PyPI](https://pypi.org/), via [pipx](https://pypa.github.io/pipx/) or [uv](https://docs.astral.sh/uv/) (using the `uv tool` command).

**Documentation**: [https://aj-white.github.io/piplexed/](https://aj-white.github.io/piplexed/)

</div>

## ⛳ Table of Contents

- [Usage](#usage)
- [Installation](#installation)
- [Why piplexed ?](#why-piplexed)
- [Caveats](#caveats)
- [License](#license)



## 🔧 Usage

### Show Outdated Packages (Tools)

Ignores prelease and dev releases by default.

#### Installed with Pipx

```console
piplexed list --outdated
```

<p align="left">
<img src="https://raw.githubusercontent.com/aj-white/piplexed/main/docs/img/piplexed-list-out.gif" alt="piplexed in action" width=750/>
</p>

#### Installed with uv
```console
piplexed list --outdated --tool uv
```

### Show outdated packages (include pre or dev releases)

#### Installed with pipx

```console
piplexed list --outdated --pre
```

<p>
<img src="https://raw.githubusercontent.com/aj-white/piplexed/main/docs/img/piplexed-list-outdated-pre.PNG" alt="pipx installed tool include prerelease" width=300/>
</p>

#### Installed with uv
```consle
piplexed list --outdated --pre --tool uv
```

<p>
<img src="https://raw.githubusercontent.com/aj-white/piplexed/main/docs/img/piplexed-list-outdated-pre-uv.PNG" alt="uv installed tool include prerelease" width=300/>
</p>

### List Installed Packages

#### With pipx

```console
piplexed list
```
Outputs similar information to `pipx list`, albeit minus the names of the binaries, in a rich table format.

<p>
<img src="https://raw.githubusercontent.com/aj-white/piplexed/main/docs/img/piplexed-list-table.PNG" width=300>
</p>


```console
piplexed list --tree
```

An optional tree flag can be passed for a tree view (less useful if there are a lot of packages)

<p>
<img src="https://raw.githubusercontent.com/aj-white/piplexed/main/docs/img/piplexed-list-tree.PNG" alt="piplexed list tree" width=200/>
</p>

#### With UV
```console
piplexed list --tool uv
```



## 👷‍♀️ Installation

**Piplexed** is designed to be installed globally via **pipx** or **uv**.

To install **piplexed**:

```console
pipx install piplexed
```

or

```console
uv tool install piplexed
```

Alternatively you can run it wihtout installation, supplying the required arguments shown below

```console
pipx run -- piplexed <ARGS>
```
or
```console
uv tool run piplexed <ARGS>
```

## ❓ Why piplexed

The name **piplexed** is a play on words, it contains the letters for pipx and I was also mildly perplexed trying to find a simpler way to identify outdated pipx installed packages, only to discover it didn't exist. Put the two together and well.... you get the idea (naming things is hard after all!).
For a longer answer see the [documentation](https://aj-white.github.io/piplexed/Why-piplexed/).


## 🩹 Caveats

**Piplexed** is a project that I built for my workflow, but it may not work for everyone.

It is only intended to work for packages that are installed from [PyPI](https://pypi.org), so will not work for local packages or git/url etc.

## 📝 License

**Piplexed** is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
