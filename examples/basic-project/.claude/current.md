# Current Project

## Project Status

Authentication MVP is working locally. Registration support is partially implemented and needs another session to complete.

## Architecture

- FastAPI service with a single entry point in `src/main.py`
- In-memory user store for the example only
- Session continuity is maintained through `.claude/current.md` and `.claude/sessions/`

## Active Problems

- `/register` still accepts malformed email input
- No rate limiting exists on `/login`
- No automated tests are wired up yet

## Important Decisions

- Keep the example intentionally small and single-file so the workflow stays easy to inspect
- Preserve `.claude/` as the continuity directory for v0.1
- Treat the archive as history and `current.md` as live truth

## Next Steps

1. Add email validation to `/register`
2. Add a basic rate-limit strategy for `/login`
3. Add one integration-style test for the login happy path
