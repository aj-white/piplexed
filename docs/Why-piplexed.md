# Why piplexed ?

## Short answer
The name **piplexed** is a play on words, it contains the letters for pipx and I was also mildly perplexed trying to find a simpler way to identify outdated pipx installed packages, only to discover it didn't exist. Put the two together and well.... you get the idea (naming things is hard after all!)

## Long answer

**Pipx** is a really useful tool, essentially any python package that has a console script entry point can be installed in its own isolated environment, but still be run directly from the command line without requiring any virtual environment activation or polluting the main python install.

When building libraries and applications I use a fairly consistent set of tools.

- [**virtualenv**](https://github.com/pypa/virtualenv) - I prefer this to the standard library [venv](https://docs.python.org/3/library/venv.html) module as it is faster at environoment creation, installs [wheel](https://github.com/pypa/wheel) by default and gives you an up to date version of [pip](https://github.com/pypa/pip).
- [**black**](https://github.com/psf/black) - consistent code formatting
- [**mypy**](https://github.com/python/mypy) - static type checking
- [**ruff**](https://github.com/charliermarsh/ruff) - code linting
- [**hatch**](https://github.com/pypa/hatch) - Starting projects, bumping versions and building packages

For personal projects, rather than having to install these packages in every project (taking up time and disk space!), they can be installed once, in a single isolated location, and used in each project thanks to [**pipx**](https://github.com/pypa/pipx).

!!! tip
    one caveat with mypy is that you have to pass it the [`--python-executable`](https://mypy.readthedocs.io/en/stable/command_line.html?highlight=python-executable#cmdoption-mypy-python-executable) flag with the path to python executable in the environment you want to run it on, otherwise it can't find helpful things like stub files.

However, over time, packages get updated, either to introduce new features or fix bugs and security issues. **Pipx** provides the following commands to update a specfic package or update all installed packages.

```console
pipx upgrade PACKAGE_NAME
pipx upgrade-all
```

Upgrading a single package, requires knowing there is an updated version on PyPI already or the `upgrade-all` command can be run periodically to always get the latest version(s). This runs the risk of a newer version (especially if it is a new major version) either breaking the workflow (due to API changes) or behaving in unexpected ways (due to changed behaviour).

In order to avoid this I would run `pipx list`, then manually check PyPI for a newer version. If there was one I'd check the release notes to see if there were any breaking changes and if all looked okay, update the package.

Having grown tired of manually checking PyPI for new versions, I wanted a more efficient solution.

Depenendcy management has always been a little bit tricky in python and there are lots of tools to manage dependencies in a virtual environment e.g. [**poetry**](https://github.com/python-poetry/poetry), [**pip-tools**](https://github.com/jazzband/pip-tools).

Even using just **pip** you can get a list of outdated packages in an environment with the command:
```console
python -m pip list --outdated
```
This will display any dependency that has a newer version on PyPI, including all package sub-dependencies.

All these tools work on a per environment basis but I was looking for a tool or way to show outdated packages installed with **pipx**, which involves multiple environments.

The `pipx list` command shows all the packages installed with **pipx** (excluding dependencies) and their versions. However there is no `outdated` option like **pip**.

### Are There Existing Solutions ?

There are a couple of issues on **pipx's** github page that have been open for a couple of years now looking at this feature but as yet no progress:

- [#149 - Feature request: Option to list available upgrades without performing them](https://github.com/pypa/pipx/issues/149)
- [#464 - Check for latest version before running with pipx run](https://github.com/pypa/pipx/issues/464)

A search of PyPI also showed no existing solutions, so I decided to build something to solve the problem.

#### Why not submit a PR instead ?

You may ask why not fix one of the above issues ?

That's a perfectly valid question. The truth is I currently don't feel like I have the skills to provide a robust enough solution that would work across multiple OS to satisfy the requirements of a package as widely used as **pipx**.
This project is an opportunity for me to develop (hack together) a solution that works for me, it is not intended to be a universal solution for all.
