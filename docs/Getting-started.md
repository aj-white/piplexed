
## Basic Usage

Now that you have **piplexed** installed, you can check for newer versions on PyPI of your installed packages/tools.

The default is to ignore pre-release versions.

/// tab | pipx installed

```console
piplexed list --outdated
```
/// details | Example Output: *list --outdated*
    type: note

<p align="center">
<a href="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list-outdated.PNG">
<img src="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list-outdated.PNG" width=300/>
</a>
</p>
///

///

/// tab | uv installed

```console
piplexed list --outdated --tool uv
```

///

/// tab | pipx and uv installed
```console
piplexed list --outdated --tool all
```
///

If you wish to include pre-release versions you can use the `--pre` flag.


/// tab | pipx installed
```console
piplexed list --outdated --pre
```

/// details | Example Output: *list --outdated --pre*
    type: note
<p align="center">
<a href="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list-outdated-pre.PNG">
<img src="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list-outdated-pre.PNG" width=300/>
</a>
</p>
///
///

/// tab | uv installed

```console
piplexed list --outdated --pre --tool uv
```

/// details | Example Output: *list --outdated --pre --tool uv*
    type: note
<p align="center">
<a href="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list-outdated-pre-uv.PNG">
<img src="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list-outdated-pre-uv.PNG" width=300/>
</a>
</p>
///
///
///

/// tab | pipx and uv installed
```console
piplexed list --outdated --pre --tool all
```

///

## Installed Tools

You can also list the installed packages/tools name, version and python version of the virtual environment.
This is similar to `pipx list` or `uv tool list`


/// tab | pipx installed

```console
piplexed list
```

/// details | Example Output: *list*
    type: note

<p align="center">
<a href="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list-table.PNG">
<img src="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list-table.PNG"/>
</a>
</p>

///
///

/// tab | uv installed

```console
piplexed list --tool uv
```

///

/// tab | pipx and uv installed
```console
piplexed list --tool all
```

///

If you prefer there is also a tree view option.

```console
piplexed list --tree
```

/// details | Example Tree Output
    type: note
<p align="center">
<a href="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list-tree.PNG">
<img src="https://github.com/aj-white/piplexed/raw/main/docs/img/piplexed-list-tree.PNG"/>
</a>
</p>

///

/// details
    type: warning
    open: True

The tree view is not recommended if there are a lot of packages to view
///

