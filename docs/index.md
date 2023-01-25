
--- 
**Documentation** For full documentation visit [mkdocs.org](https://www.mkdocs.org).

**Source Code** [https://github.com/aj-white/piplexed](https://github.com/aj-white/piplexed)

---

# Welcome to Piplexed


## Overview

Piplexed is a command line tool to identify outdated python packages, installed from [PyPI](https://pypi.org/), via [pipx](https://pypa.github.io/pipx/).

### What is pipx ?

Pipx is a tool to help you install applications written in Python, into isolated environments with the ability to run them globally with no environment activation necessary.


## Requirements

- Python 3.7+
- At least one python packaged installed with `pipx`

## Installation

Piplexed is designed to be installed globally via `pipx`.

To install `piplexed` with `pipx`

```console
pipx install piplexed
```


## Examples

Show version and python version of packages installed with `pipx`
```console
piplexed list
```
<p align="center">
<a href="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list.PNG">
<img src="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list.PNG"/>
</a>
</p>

Show the installed version of a package and the latest PyPI verision, ignoring pre-release and dev versions
```console
piplexed list --outdated
```

<p align="center">
<a href="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list-outdated.PNG">
<img src="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list-outdated.PNG" width=300/>
</a>
</p>

Show the installed version of a package and the latest PyPI verision, including pre-release and dev versions
```console
piplexed list --outdated --pre
```

<p align="center">
<a href="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list-outdated-pre.PNG">
<img src="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list-outdated-pre.PNG" width=300/>
</a>
</p>

## License

This project is licensed under the terms of the MIT license.
