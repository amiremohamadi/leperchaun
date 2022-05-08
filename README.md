<p align="center"><img src=".github/leperchaun.png" width="300"></p>

# Leperchaun
modular bug bounty automation. the idea is to keep modules small and simple to
keep you away from thinking about the core concepts. also the goal is to make
the whole process async.

## Usage
install the requirements:
```sh
$ pip install -r requirements.txt
```

run the following command:
```sh
$ python hunter -h
```

which will show you this:
```sh
usage: hunter [-h] [--config CONFIG] --domain DOMAIN

pipeline runner

options:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        pipeline config file
  --domain DOMAIN, -d DOMAIN
                        domain to be hunted
```

## Config
the flow and usage of modules is configurable. the config is sth like this:
```json
{
    "name": "default pipeline",
    "version": "0.0.1",
    "logger": {
        "token": "BOT_TOKEN",
        "error_log": "ERROR_LOG_FILE"
    },
    "pipeline": [
        {
            "name": "enumer",
            "startJob": true,
            "pipeTo": "flinks"
        },
        {
            "name": "flinks",
        }
    ]
}
```

- `name` is mandatory
- `pipeTo` is optional
- `startJob` is mandatory and MUST be used only once

## Contributing
clone the source:
```sh
$ git clone git@github.com:amiremohamadi/leperchaun.git && cd leperchaun
```

do some hacking on the source. a new module or edit on the core.
then run following commands:
```sh
$ make test
$ make fmt
```
don't forget to write tests for your changes.
