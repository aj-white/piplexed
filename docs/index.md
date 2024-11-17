# Piplexed

--- 
**Documentation**: [https://aj-white.github.io/piplexed/](https://aj-white.github.io/piplexed/).

**Source Code**: [https://github.com/aj-white/piplexed](https://github.com/aj-white/piplexed)

---

<p align="center">
<img src="https://raw.githubusercontent.com/aj-white/piplexed/main/docs/img/piplexed-list-out.gif" alt="piplexed in action"/>
</p>



## Who is this for ?

Anyone who has installed python packages/tools via [pipx](https://github.com/pypa/pipx) or [uv tool](https://github.com/astral-sh/uv) that wants to check if newer versions are available on [PyPI](https://pypi.org/) without the need to blindly run an update command.

## Overview

### Requirements

- Python 3.9+
- At least one python package installed with **pipx** or **uv**

/// note | Windows Users

If you experience issues with [strange characters being shown](https://github.com/aj-white/piplexed/issues/21), this is most likely due to Windows ability to handle utf-8 encoding.
If this happens you may need to change the code page by typing `chcp 65001` or use a prompt like [ohmyposh](https://ohmyposh.dev/) which does this for you.
///


**Piplexed** is a command line tool to identify outdated python packages/tools, installed from [PyPI](https://pypi.org/), via [pipx](https://github.com/pypa/pipx) or [uv](https://github.com/astral-sh/uv). It displays its output as a [rich](https://github.com/Textualize/rich) printed table by default, with an alternative tree output available if desired.


### What do we mean by package/tools ?

We define *package/tools* as python packages that provide a command line interface, only these types of packages can be installed via `pipx` or `uv tool`.

### What is pipx ?

`pipx` is a tool to help you install applications written in Python, into isolated environments with the ability to run them globally with no environment activation necessary.

### What is uv ?

`uv` is a python package and project manager. written in [rust](https://www.rust-lang.org/). `uv` has a `uv tool` interface which like `pipx`, installs applications into an isolated virtual environment and allows them to be run globally.


## License

This project is licensed under the terms of the MIT license.
