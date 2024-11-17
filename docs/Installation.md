**Piplexed** is designed to be installed globally via [pipx](https://github.com/pypa/pipx) or [uv](https://github.com/astral-sh/uv).

Both `pipx` and `uv` (via `uv tool`) allow the install Python CLI applications globally in isolated virtual environments.

/// tab | pipx

```console
pipx install piplexed
```
///

/// tab | uv

```console
uv tool install piplexed
```
///


Alternatively you can run **piplexed** wihtout installation, supplying the required arguments shown below


/// tab | pipx
```console
pipx run -- piplexed <ARGS>
```
///

/// tab | uv
```console
uv tool run piplexed <ARGS>
```
///