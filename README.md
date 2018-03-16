# Snake Tail

The command line interface to Snake. If Web UIs and cURL are not your thing, then this is for you!

## Installation

To install perform the following:

```bash
pip3 install git+https://github.com/countercept/snake
```

## Usage

Snake Tail supports the following, as displayed by its usage page:

```bash
snake-tail -h
usage: snake-tail [-h] [--insecure] [--json]
                  {command,download,file,memory,note,scale,scales,store,upload}
                  ...
positional arguments:
  {command,download,file,memory,note,scale,scales,store,upload}
                        command help
    command             execute a command on a sample in snake
    download            download a sample from snake
    file                get information about a file from snake
    memory              get information about a memory from snake
    note                get the note for a sample
    scale               interact with snake's scales
    scales              list installed scales
    store               get information about samples in snake
    upload              upload a sample to snake
optional arguments:
  -h, --help            show this help message and exit
  --insecure            ignore ssl verification
  --json                return all output in json (where applicable)

```

By default, Snake Tail will try to communicate with Snake over `localhost:5000` this can be overridden by setting the environment file `SNAKE_URL`.

```bash
export SNAKE_URL='http://api.snake.example.com'
```
