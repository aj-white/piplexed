# Command Line Options

The commands of *piplexed* can been seen by running `piplexed --help`

For each each command running `--help` will show all the command line options, which are detailed below.
```shell
$ piplexed list --help
$ piplexed version --help
```

## piplexed list

List all packages installed via pipx (output in table format by default)
```shell
$ piplexed list
```

### `--outdated` / `-O`
Show any packages installed via pipx that have a newer version on PyPI
```shell
$ piplexed list --outdated
```


### `--pre` / `P`
Include pre-release or dev-releases when determining newer versions (use in conjunction with `--outdated`)
```shell
$ piplexed list --outdated --pre
```

### `--tree` / `-T`
Output as a rich tree (less useful if lots of packages)
```shell
$ piplexed list --tree
$ piplexed list --outdated --tree
```

## piplexed version

Show version

```shell
$ piplexed version
0.1.2
```