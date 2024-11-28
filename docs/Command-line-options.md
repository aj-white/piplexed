# Command Line Options


## Usage

```console
piplexed [COMMAND] <OPTIONS>
```

The commands of **piplexed** can been seen by running `piplexed --help`

For each each command running `--help` will show all the command line options, which are detailed below.
```shell
piplexed list --help
piplexed version --help
```

## piplexed list

#### Usage

```console
piplexed list <OPTIONS>
```

#### Options:

|**Name**|**Type**|**Descrtiption**|**Default**|
|---|---|---|---|
`--outdated`, `-O`|boolean|Check PyPI for newer versions of installed packages/tools (*installed tools not available on PyPI are ignored during check*). If `False` list packages/tools installed with specified tool.| `False`
`--pre`, `-P`|boolean|include pre-releases in check for newer versions|`False`
`--tree`, `-T`|boolean|Show results in a tree format|`False`
`--tool`|text|Choose which tool packages werre installed with. Options are `pipx`, `uv`, `all`|`pipx`


## piplexed version

#### Usage

```console
piplexed version
0.1.2
```