# `swarm-checkin-post-man`

## Setup

### Server environments

- Copy `.env.sample` to `.env` and then fill in the necessary values.

```shell
make setup

```

- Install dependencies

```shell
make install
```

### Swarm environments

- Swarm redirect URL
- Swarm push URL

## Run

```shell
uv run fastapi run src/scpm/run.py
```
