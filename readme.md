# Command Center

A lightweight Flask dashboard for managing remote servers. Configuration and server metadata
are stored under `~/.pcc` so you can sync them across machines.

## Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
```

Copy `static/settings.example.json` (if available) or create `~/.pcc/settings.json` with an
`ssh_user` and `fetch_command`. The fetch command can reference `{server_path}` which will be
replaced with the local path where server metadata is stored.

Run the development server:

```bash
python main.py
```

## Quality checks

```bash
. .venv/bin/activate
ruff check .
pytest
```

GitHub Actions (see `.github/workflows/ci.yml`) executes the same commands on every push and
pull request, and Dependabot keeps pip and workflow dependencies current.
