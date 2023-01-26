# Why piplexed ?

## Short answer
The name `piplexed` is a play on words, it contains the letters for pipx and I was also mildly perplexed trying to find a simpler way to identify outdated pipx installed packages, only to discover it didn't exist. Put the two together and well.... you get the idea (naming things is hard after all!)

## Long answer

I use a fairly consistent set of python packages when building libraries and applications.

- [virtualenv](https://github.com/pypa/virtualenv) - I prefer this to the standard library [venv](https://docs.python.org/3/library/venv.html) module as it is faster at environoment creation, installs [wheel](https://github.com/pypa/wheel) by default and gives you an up to date version of [pip](https://github.com/pypa/pip).
- [black](https://github.com/psf/black) - Consistent code formatting
- [mypy](https://github.com/python/mypy) - static type checking
- [flake8](https://github.com/PyCQA/flake8) or [ruff](https://github.com/charliermarsh/ruff) - code linting
- [hatch](https://github.com/pypa/hatch) - Starting projects, bumping versions and building packages

Rather than having to install these packages in every project (taking up time and disk space!), they can be installed once and run everywhere using [pipx](https://github.com/pypa/pipx). Pipx is really useful, essentially any python package that has a console script entry point can be installed in it's own isolated environment but still be run directly from the command line without requiring any virtual environment activation or polluting the main python install.


!!! tip
    one caveat with mypy is that you have to pass it the [`--python-executable`](https://mypy.readthedocs.io/en/stable/command_line.html?highlight=python-executable#cmdoption-mypy-python-executable) flag with the path to python executable in the environment you want to run it on, otherwise it can't find helpful things like all the stub files you installed (took a while to work that out so have that tip for free)

Depenendcy management has always been a little bit tricky in python and there are lots of tools to manage dependencies in a virtual environment e.g. [poetry](https://github.com/python-poetry/poetry), [pip-tools](https://github.com/jazzband/pip-tools).
With just `pip` you can get a list of outdated packages in an environment with the command:
```console
python -m pip list --outdated
```
This will display any dependency that has a newer version on PyPI, including all package sub-dependencies.

All these tools work on a per environment basis and I was looking for a tool or way to show outdated packages installed with `pipx`.

`pipx` has a `list` command which shows all the packages installed with pipx (excluding dependencies) and their versions. However it doesn't have an `outdated` option like `pip`.

It is of course a slightly different problem, rather than dealing with a single environment, there are multiple environemnts (one for every installed package). Each of those environments has the installed package and all it's dependencies but we only really care about the top level package.

#### Am I the only one looking for this ?

There are a couple of issues on pipx's github page that have been open for a couple of years now looking at this feature but as yet no progress:

- [#149 - Feature request: Option to list available upgrades without performing them](https://github.com/pypa/pipx/issues/149)
- [#464 - Check for latest version before running with pipx run](https://github.com/pypa/pipx/issues/464)


#### How was this managed before piplexed ?

Essentially I would run `pipx list` command then manually check PyPI for a newer version. If there was one I'd check the release notes to see if there were any breaking changes and if all looked okay, update the package with the `pipx upgrade <package>` command.

Having grown tired of manually checking PyPI for new versions, I decided to hack together my own solution.


#### Why not submit a PR instead ?

You may ask why not fix one of the above issues ?
That's a perfectly valid question. The truth is I currently don't feel like I have the skills to provide a robust enough solution that would work across multiple OS to satisfy the requirements of a package as widely used as `pipx`.
This is a solution that works for me and while I have gone some way to test it there are some caveats.
