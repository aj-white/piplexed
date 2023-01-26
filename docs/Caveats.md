# Caveats

Piplexed is a solution that works for my workflow, but it may not work for everyone.

These are some things to be aware of:

- Only works for packages that are on [PyPI](https://pypi.org), does not work for local packages or git/url etc.
- Currently no optimisation, so it can be a little slow if you have a lot of pipx installed packages.
- Has only been tested on windows 10, *as `piplexed` uses that same method of venv discovery as `pipx` it should also work on macOS and linux but there are no guarantees*.