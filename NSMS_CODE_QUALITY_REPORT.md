# NSMS Code Quality Review Report

Date: 2026-11-24  
Project: Networked Student Management System (NSMS)

## 1. Scope

Reviewed the full codebase for readability and maintainability:

- `server.py`
- `Client/` (CLI menus and TCP request helper)
- `services/` and `repositories/`
- `database/` and `models/`
- `frontend/gateway.py`, `frontend/README.md`, and `frontend/js/`
- all Python test modules

The review focused on the requested human-readable qualities: simple logic, meaningful names, clear SQL, useful comments, consistent formatting, and no dead weight. The existing architecture, request/response envelope, routes, payload keys, validation rules, database schema, and role checks were preserved.

Pre-existing uncommitted work in the working tree (environment-based database credentials, protocol framing changes, validation hardening, and the new isolated tests) was left intact.

## 2. Overall assessment

The project already has a sensible layered structure: socket server → services → repositories → database, with an HTTP gateway for the browser and a separate CLI client. Most functions are short and single-purpose.

The main problem was not the architecture. It was presentation:

- change-history banners such as `===== ADDED: ... =====` appeared throughout Python, SQL, Markdown, and JavaScript files;
- several local variables mirrored abbreviated protocol keys (`t_id`, `co_id`, `j_o_d`), which made request branches harder to read;
- the gateway module docstring described how the file was introduced rather than what it does;
- password-hashing parameters were repeated as bare numbers;
- one tuple position was used directly in two authorization checks without a name;
- a few imports, long lines, and SQL strings were formatted inconsistently.

No public function, route, table, column, payload key, or client-facing message was renamed or removed.

## 3. Changes made

| Area | Finding | Action taken |
| --- | --- | --- |
| All layers | Stale `ADDED`/`UPDATED` banners described change history, not current behavior. | Removed them from `server.py`, `Client/menu.py`, services, repositories, tests, `database/schema.sql`, `frontend/README.md`, and `frontend/js/app.js`. |
| `server.py` | Standard-library imports, project imports, and history comments were mixed together. | Reordered imports into stdlib and project groups. |
| `server.py` | `Login` and `Logout` bypass access checks intentionally, but the reason was not stated. | Added one concise comment explaining that they manage the session itself. |
| `server.py` | Locals such as `t_id`, `t_name`, `j_o_d`, `co_id`, and `co_name` were hard to scan. | Renamed locals to `teacher_id`, `teacher_name`, `joining_date`, `course_id`, and `course_name`. Wire keys remain unchanged. |
| `server.py` | The teacher ID in an `s_data` row was accessed as `existing["data"][3]` in two places. | Added `teacher_owns_result()` with a short docstring. The same check and the same responses are preserved. |
| `server.py`, repositories, services | Some lines exceeded 100 characters. | Wrapped long calls and SQL strings using adjacent string literals; the resulting SQL text is unchanged. |
| `frontend/gateway.py` | The module docstring contained defensive patch narration and setup history. | Replaced it with a short description of the gateway's role and environment overrides. |
| `frontend/gateway.py` | `socket.create_connection(..., timeout=10)` was followed by a redundant `settimeout(10)`. | Removed the redundant call. |
| `frontend/gateway.py` | `JSONDecodeError` is a subclass of `ValueError`, so both were listed in one `except`. | Simplified to `except ValueError`. Behavior is unchanged. |
| `frontend/gateway.py` | `sanitize_response()` mutates its argument, which its old docstring did not say. | Clarified the docstring. No sanitization logic changed. |
| `services/auth_services.py`, `services/student_services.py` | PBKDF2 iterations and salt size were repeated as bare numbers in security-critical code. | Introduced `PASSWORD_ITERATIONS = 200000` and `SALT_BYTES = 16` in each module. Hash format and parameters are unchanged. |
| Services and repositories | Import grouping and blank lines were inconsistent. | Normalized import order and wrapping without changing behavior. |
| `database/schema.sql` | A stale note described a past schema edit. | Replaced it with a current table-purpose comment for `teacher_student_allocation`. |
| Tests and docs | History banner comments added noise without explaining behavior. | Removed only those comments; assertions, setup, and test intent were unchanged. |

## 4. Deliberate non-changes

The following were left alone because changing them would be a wider behavioral or architectural refactor rather than a readability fix:

- **Route policy and dispatch are both expressed in `server.py`.** A single route registry would reduce duplication, but it would change control flow in the protocol core. The current explicit chain is easier to audit and was preserved.
- **Some services return raw `str(e)` messages.** These strings are part of existing client-visible behavior. They were not changed even where neighboring functions use fixed messages.
- **Validation is repeated across service modules.** Shared validators would add cross-module coupling. Named constants were introduced where the repetition was security-sensitive; all limits and messages remain exactly as they were.
- **A few repository queries use `SELECT *`.** The tuple order is consumed by services and the frontend. Replacing it with explicit columns should be a separate contract-review task.
- **The legacy `models/` classes are not imported by the running application.** They were kept for compatibility rather than deleted or marked with uncertain labels.
- **`frontend/js/app.js` and `Client/menu.py` remain large.** Only stale comments were removed. Dividing them into new view/menu abstractions would risk changing data attributes, prompts, or request flow.
- **Database-backed tests open MySQL at import time.** Moving this behind fixtures would change the test architecture. The current behavior was preserved and is documented in the verification section below.

No validation, authorization, transaction handling, socket framing, response key, or database relationship was weakened or removed.

## 5. Verification

Commands were run from the project root.

Isolated tests that do not require MySQL:

```text
python -B -m pytest -q tests/test_client_request.py tests/test_gateway.py tests/test_server_protocol.py tests/test_service_validation.py
............                                                             [100%]
12 passed in 2.32s
```

Full suite:

```text
python -B -m pytest -q --tb=no
7 errors during collection
```

All seven errors are MySQL connection failures at test import time:

```text
mysql.connector.errors.ProgrammingError: 1045 (28000):
Access denied for user 'root'@'localhost' (using password: NO)
```

This is identical to the baseline result before the cleanup. The database-backed tests require `NSMS_DB_USER`, `NSMS_DB_PASSWORD`, and related environment variables, plus a running MySQL server with the `SCHOOL_NET` schema. No database was available in this environment, so those tests could not be executed.

Additional checks:

- `python -m compileall -q server.py Client frontend/gateway.py services repositories database models tests` — passed. Generated bytecode changes were restored/removed afterward because some `.pyc` files are tracked in the repository.
- `node --check frontend/js/app.js` — passed.
- `git diff --check` — no whitespace errors.

The isolated suite was re-run after each meaningful source change.

## 6. Result

The codebase now reads like a maintained student project: the history markers are gone, names describe their values, comments explain intent where it is not obvious, and repeated security constants are named. Functionality, protocols, schema, validation, and public interfaces remain unchanged.
