# Changelog

## [Unreleased](https://github.com/aj-white/piplexed/compare/v0.6.0...HEAD)

- Use `uv` with nox


## [0.6.0](https://github.com/aj-white/piplexed/compare/v0.5.0...v0.6.0)


## Added

- Performance improvement, refactored to multi-threaded design.
- Progress bar when getting data from pypi
- Added python 3.13 support

## Changed
- Updated tests and added explanatory docstrings

## Deprecated

- Removed python 3.8 support as end of life

## [0.5.0](https://github.com/aj-white/piplexed/compare/v0.4.0...v0.5.0)

### Added
- Test against current and previous pipx metadata versions

### Changed
- Updated how pipx home is located, now in line with `pipx` package as it is dependent on operating system
- Warn user if pipx metadata version is not tested against.

### Fixed
- Handle when multiple json files are present in pipx venv folder

## [0.4.0](https://github.com/aj-white/piplexed/compare/v0.3.0...v0.4.0)

### Changed
- Table is now the default option for `list` command, tree view available via `--tree` option. #40
- ReadME and documention updated reflecting change to table default.

### Added
- Ignore PyPI packages whose version does not follow [PEP 440](https://peps.python.org/pep-0440/)

## [0.3.0](https://github.com/aj-white/piplexed/compare/v0.2.0...v0.3.0)

### Changed
- Minor docs fix for shell examples
- Update python version colour in `piplexed list` to a lighter green.

### Deprecation
- Deprecation warning added as the table view will become the default in v0.4.0

## [0.2.0](https://github.com/aj-white/piplexed/compare/v0.1.2...v0.2.0)

### Added

- Support for python 3.12
- Table option for CLI output

### Changed

- Updated docs for windows display issues


## [0.1.2](https://github.com/aj-white/piplexed/compare/v0.1.1...v0.1.2) - 2023-06-16

### Fixed

- Incorrect `python_requires` in `pyproject.toml`

## [0.1.1](https://github.com/aj-white/piplexed/compare/v0.1.0...v0.1.1) - 2023-06-15

### Fixed

- Erroneous github repo link in `pyproject.toml`

## [0.1.0](https://github.com/aj-white/piplexed/tag/v0.1.0) - 2023-06-12

### Fixed

- Handle `NoSuchProjectError` by not sending non-pypi packages (locally installed wheels) to PyPI API.
- Various linitng and mypy errors have been squashed.



### Added

- Added user cache directory using [platformdirs](https://github.com/platformdirs/platformdirs)
- Add [nox](https://github.com/wntrblm/nox) as test and lint runner
- Add github actions for linting and tests

### Changed

- `remove_expired_responses()` being depracted in `requests-cache` replaced with `cache.delete(expired=True)`


## 0.0.2

⬆ Bump simple-pypi to 1.1.0