# Piplexed

--- 
**Documentation**: [https://aj-white.github.io/piplexed/](https://aj-white.github.io/piplexed/).

**Source Code**: [https://github.com/aj-white/piplexed](https://github.com/aj-white/piplexed)

---



## Overview

**Piplexed** is a command line tool to identify outdated python packages, installed from [**PyPI**](https://pypi.org/), via [**pipx**](https://pypa.github.io/pipx/). It displays it's output as a nice [**rich**](https://github.com/Textualize/rich) printed tree by default, with an alternative table output if needed.

### What is pipx ?

**Pipx** is a tool to help you install applications written in Python, into isolated environments with the ability to run them globally with no environment activation necessary.


## Requirements

- Python 3.8+
- At least one python package installed with **pipx**

!!! note "Windows Users"

    If you experience issues with [strange characters being shown](https://github.com/aj-white/piplexed/issues/21), this is most likely due to Windows ability to handle utf-8 encoding.
    If this happens you may need to change the code page by typing `chcp 65001` or use a prompt like [ohmyposh](https://ohmyposh.dev/) which does this for you.

## Installation

**Piplexed** is designed to be installed or run via **pipx**.

To install **piplexed** with **pipx**

```shell
$ pipx install piplexed
```

Or to run **piplexed** without installing

```shell
$ pipx run -- piplexed list --outdated
```


## Basic Usage

Show the installed package version and python version of the virtual environment of packages installed with **pipx**.
(*Similar to the `pipx list` command*).
```shell
$ piplexed list
```
<p align="center">
<a href="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list.PNG">
<img src="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list.PNG"/>
</a>
</p>

Show the installed package version and the latest PyPI version, excluding pre-release and dev-release versions.
```shell
$ piplexed list --outdated
```

<p align="center">
<a href="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list-outdated.PNG">
<img src="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list-outdated.PNG" width=300/>
</a>
</p>

Show the installed package version and the latest PyPI version, including pre-release and dev-release versions.
```shell
piplexed list --outdated --pre
```

<p align="center">
<a href="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list-outdated-pre.PNG">
<img src="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list-outdated-pre.PNG" width=300/>
</a>
</p>

## License

This project is licensed under the terms of the MIT license.
