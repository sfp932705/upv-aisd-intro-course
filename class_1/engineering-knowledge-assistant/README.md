# Engineering Knowledge Assistant — Class 1 starter

This is the **Class 1 homework repository** and the first building block of the course. In this assignment, you
implement a small, testable document catalogue. The RAG functionality is introduced in Class 3; do not implement AI
features here.

## Goal

Complete `src/engineering_knowledge_assistant/catalog.py` so it scans a directory and creates a deterministic manifest
of supported documents (`.pdf`, `.txt`, `.md`). The acceptance tests are provided; the four implementation functions
contain TODOs.

## Requirements

- Linux, macOS, or Windows with Ubuntu on WSL2
- Python >= 3.12
- Git, GNU Make and [uv](https://docs.astral.sh/uv/)
- IDE configured to use the project's `.venv` interpreter

## Setup

Once you have cloned the repository, head over to the *engineering-knowledge-assistant* directory and from there run:

```bash
make install-test
```

`make install-test` runs the Makefile's `uv sync` steps: it installs the default development tools and the test
dependency group and creates `.venv/`.

## Course Makefile

The supplied Makefile is intentionally retained as the team's command interface:

```bash
make install-test  # install default + test dependency groups
make lint          # Ruff + mypy
make format        # Ruff formatting + import sorting
make test          # pytest with coverage
make clean         # remove local caches and coverage output
```

`make lint` should pass on the starter. The tests are expected to fail until you implement the TODO functions.

## Your tasks

Implement the four TODOs in `src/engineering_knowledge_assistant/catalog.py`:

1. `is_supported_document`: accept regular files with `.pdf`, `.txt`, `.md` extensions, case-insensitively.
2. `discover_documents`: recursively find supported files, sorted by relative POSIX path. Return `[]` when the root does
   not exist; raise `NotADirectoryError` if it exists but is not a directory.
3. `describe_document`: return a `DocumentInfo` with the original filename, relative POSIX path, lower-case extension
   and file size. Raise `ValueError` for unsupported files or paths outside the root.
4. `build_manifest`: compose the previous functions; do not duplicate their logic.

Read the tests before coding. They define the expected behavior. Do not weaken or edit the provided tests to make them
pass. Add at least two extra tests for edge cases of your choice.

## Suggested workflow

```bash
git checkout -b feat/document-catalog
make lint
make test  # expected to fail until TODOs are implemented. Implement one function at a time
make format
make lint
make test
uv run pre-commit install
uv run pre-commit run --all-files
```

Use small Conventional Commits, for example:

```text
feat(catalog): detect supported document types
feat(catalog): discover documents recursively
feat(catalog): build document manifest
test(catalog): cover additional path edge cases
```

Push your feature branch to GitHub using the repository's HTTPS remote and open a pull request. Do not commit `.venv/`,
secrets, IDE caches or local data.

## Acceptance criteria

- [ ] All provided tests pass.
- [ ] `make lint` passes.
- [ ] `make format` produces no further changes on a second run.
- [ ] At least two additional tests are included.
- [ ] At least three meaningful Conventional Commits are present.
- [ ] A feature branch is pushed and a pull request is opened.
- [ ] README explains setup, commands and the behavior implemented.

## Questions for the pull request

1. Why is `uv.lock` committed while `.venv/` is ignored?
2. What is the difference between Ruff and mypy?
3. What do the local hooks check, and why will we still need CI later?
4. Which edge cases did your additional tests cover?

Submit the pull request URL and a short note about one bug or edge case you encountered.

## Completed implementation

The document catalogue recursively discovers `.pdf`, `.txt`, and `.md`
files, accepting uppercase and lowercase extensions.

Documents are sorted by their relative POSIX paths. Each manifest entry
contains the original filename, relative path, lowercase extension,
and file size in bytes.

Missing root directories return an empty list. A root that is a file
raises NotADirectoryError. Unsupported documents and paths outside
the root raise ValueError.

## Setup and checks

Requirements: Python >= 3.12, uv, Git, and GNU Make.

Run these commands from class_1/engineering-knowledge-assistant:

```bash
make install-test
make format
make lint
make test
```

In VS Code, select `.venv/bin/python` as the Python interpreter.

## Additional tests

Two additional tests cover:
- An empty folder produces an empty manifest.
- A nonexistent PDF file is rejected.

Validation: all 12 tests and the lint checks passed.