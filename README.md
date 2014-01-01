# Business Directory CLI

Search a small business directory using parameterized SQLite queries and keyset pagination.

Uses Python 3.10+ and its standard library only. No package installation, virtual
environment, external server, Redis, Celery, or network access is required.

## Run

```console
python -m directory_lab --help
python -m directory_lab examples/sample.json
python -m directory_lab --check-fixtures fixtures/cases.jsonl
python generate_fixtures.py --count 20
python -m unittest discover -s tests -v
```

Run from this directory. The optional path defaults to `-`, which reads JSON from
stdin. Output is JSON or a fixture-check summary. Exit codes are 0 success,
1 file failure, and 2 invalid input. Examples and fixtures contain generated data.

Uses an in-memory SQLite database for each invocation; it does not save a production directory. Input has businesses plus optional search, city, category, after_id, and limit. IDs must be unique positive integers; pages contain at most 50 rows. Search treats SQL punctuation literally and is case-insensitive for ASCII letters. next_cursor is the last returned ID only when another matching row exists.

## Learning focus

The modeled transition from Python/web fundamentals to SQL-backed listing APIs. This is an independent concept exercise based on the modeled
roadmap. It makes no claim to be employer-owned or period-authentic production code.

## Structure

- `directory_lab/core.py`: validated parsing, storage, or state transitions.
- `directory_lab/cli.py`: JSON command interface.
- `directory_lab/generate_fixtures.py`: original deterministic validation cases.
- `directory_lab/fixture_check.py`: expected-output/error checks.
- `fixtures/cases.jsonl`: 367 generated cases, with explicit descriptions.
- `tests/`: independently selected boundaries and the complete corpus check.

Branches `feature/core`, `feature/cli`, `data/fixtures`, and `docs/usage` retain
snapshots; `main` contains the complete tool. Dates and provenance are also recorded
in TIMELINE.json. Many data cases share a scenario; they are not separate features.

Keep changes focused, use actual dates for new work, and add a regression test
for changed behavior. Licensed under [MIT](LICENSE).

[History and provenance](HISTORY.md).
