# `swarm-checkin-post-man`

## Setup

### Server environments

```shell
pip install -U pip poetry
poetry install
```

```shell
cp .env.example .env
```

### Swarm environments

- Swarm redirect URL
- Swarm push URL

## Run

```shell
fastapi dev scpm/run.py
```
