# NSMS Functionality Audit

## Executive summary

The project uses the confirmed architecture: browser or CLI frontend → HTTP
gateway (browser only) → TCP/JSON server → service/repository modules → MySQL.
The gateway and the TCP server are separate processes. The repositories use
parameterized SQL.

The audit found and fixed communication, validation, password-exposure, and
nullable-mark handling bugs without changing the existing database schema.
The isolated regression suite passes. Database-backed CRUD/authentication and
full end-to-end testing are **blocked**: the server cannot authenticate to the
local MySQL instance without a configured `NSMS_DB_PASSWORD`, and the existing
integration tests connect to the configured database during test collection
and then create/delete records. They were not run against an unknown database.

## Feature status

`PASS` means a tested behavior passed. `PARTIAL` means some behavior was
verified but the complete feature was not. `BLOCKED` means the feature exists
in source but could not be safely tested end to end. `NOT IMPLEMENTED` means
there is no corresponding complete feature in the current project.

| Feature | Implemented? | Tested? | Working? | Problems Found | Fix Applied |
| --- | --- | --- | --- | --- | --- |
| Student add/search/list/update/delete | BLOCKED (implemented) | No database-backed test; existing CRUD test was not run | BLOCKED | Requires MySQL credentials; student reads previously selected every column | Student reads now return only public profile columns; database execution still needs verification |
| Student login and session authentication | BLOCKED (implemented) | No database-backed login test | BLOCKED | Login depends on a valid `users` row and the expected PBKDF2 hash format; no initial-admin setup route | Database credentials moved to environment variables; no auth schema or records changed |
| Student access to own profile/results | BLOCKED (implemented) | Authorization path reviewed; no server/database E2E test | BLOCKED | Student ID ownership checks exist, but were not exercised against a live server | None; live role/ownership testing remains required |
| Teacher add/search/list/update/delete | BLOCKED (implemented) | No database-backed test | BLOCKED | Existing tests write to MySQL and were not safe to run here | Input lengths and numeric ranges now match schema limits |
| Teacher allocated students and associated courses | BLOCKED (implemented) | No database-backed test | BLOCKED | Allocation response includes course details; runtime table/data not verified | Gateway now permits the server routes |
| Teacher credential provisioning | NOT IMPLEMENTED | No | NOT IMPLEMENTED | No teacher credential setup screen/request exists; teacher login requires a pre-created `users` row | Not added |
| Course add/search/list/update/delete | BLOCKED (implemented) | No database-backed test | BLOCKED | Existing tests require an isolated MySQL database | Input lengths and finite fee ranges now validated |
| Student/teacher/course allocation add/list/remove | BLOCKED (implemented) | No database-backed test | BLOCKED | Composite key and foreign keys are defined in schema, but live table state is unknown | Gateway now permits all existing allocation routes |
| Allocation update | NOT IMPLEMENTED | No | NOT IMPLEMENTED | Only add, list, and remove operations exist | Not added |
| Course enrollment add/list/remove | BLOCKED (implemented) | No database-backed test | BLOCKED | Existing database may not yet contain `student_course_enrollment` | Gateway now permits the existing enrollment routes; no migration was applied |
| Marks add/view/update/delete | BLOCKED (implemented) | No database-backed test | BLOCKED | Foreign-key validation and persistence require MySQL | Input parsing rejects booleans/fractional IDs; non-finite/out-of-range marks are rejected |
| Marks validation | PARTIAL | Unit tests cover NaN/infinity rejection and invalid TCP IDs; FK checks were not run | PARTIAL | `s_data.marks` is nullable and has no database `CHECK` constraint | Service validation rejects non-finite values; result calculations now ignore NULL marks |
| Individual result calculation | PARTIAL | Mocked NULL-mark case tested; no database calculation tested | PARTIAL | Database values and real calculation output remain unverified | Empty/NULL-only marks now return “no marks found” |
| Topper and per-course toppers | PARTIAL | Mocked NULL-mark case tested; no database query tested | PARTIAL | Live ranking and tie behavior remain unverified | NULL marks are excluded; absent valid marks no longer cause numeric conversion failures |
| Class result statistics | PARTIAL | Mocked NULL-only case tested; no database query tested | PARTIAL | Live aggregation and class averages remain unverified | NULL-only rows are excluded and empty statistics return an explicit failure |
| Password hash protection in student responses | PARTIAL | Gateway sanitizer test passed; database/CLI query not executed | PARTIAL | Previously, `SELECT *` returned legacy `password_hash` values to the TCP client | Student repository selects only `id`, `name`, `age`, and `user_name` |
| Logout | PARTIAL | Browser API network-failure behavior tested with Node; server session invalidation not tested | PARTIAL | The UI previously displayed success when gateway logout failed | UI now reports that only local session clearing was confirmed |
| SQL injection resistance | PARTIAL | Repository SQL reviewed; no live database tests | PARTIAL | Runtime behavior could not be exercised | Repository query values use parameter placeholders; no SQL construction changes were needed |
| Gateway command routing and malformed requests | PASS (gateway scope) | HTTP route forwarding, allowlist, malformed shapes, unsupported command, and large fake TCP response tested | PASS (gateway scope only) | Live server/database route execution not verified | Gateway allowlist and request-shape checks aligned with implemented server routes |
| Full browser → gateway → server → MySQL flow | BLOCKED | No safe isolated DB configuration available | BLOCKED | Existing ports are occupied and the database password is not configured in this environment | No production requests or database mutations were made |

## Bugs found and changes made

1. **Gateway rejected most existing frontend operations.** Its allowlist covered
   only eight commands while the UI used the teacher, course, allocation,
   enrollment, credential, marks-editing, and analytics routes. The allowlist
   now includes every request routed by `server.py`.
2. **Malformed gateway JSON shapes could terminate an HTTP handler without a
   response.** Top-level objects, command types, data objects, and a 1 MiB body
   limit are now checked before forwarding.
3. **TCP requests and responses could be truncated.** The server now reads a
   complete JSON request across multiple receives, with a 1 MiB request cap;
   the CLI sends a newline delimiter and reads responses until socket close.
4. **Boolean/fractional IDs could be silently converted to integers.** Server
   payload parsing now rejects booleans and non-integer numeric values.
5. **NaN/infinite numeric values could bypass ordinary range comparisons.**
   Marks, fees, and salaries now require finite values; decimal-backed fee and
   salary limits and relevant text-column lengths are checked before writes.
6. **Student queries exposed legacy password hashes.** Student reads now select
   only profile columns; the gateway continues to strip hash-like keys.
7. **Logout failures were reported as success.** The browser clears its local
   session but now returns and displays an explicit warning when it cannot
   confirm server-side logout.
8. **NULL marks could break calculations and analytics.** Queries and service
   handling now exclude or explicitly reject empty/NULL-only result data.
9. **Database credentials were embedded in source.** Connection settings now
   use `NSMS_DB_*` environment variables, and a `requirements.txt` manifest
   plus setup instructions were added. The previously committed credential is
   still present in Git history; rotate it and handle history cleanup according
   to your repository policy.

## Changes by file

| File | Change |
| --- | --- |
| `server.py` | Added bounded complete-request reading, JSON-shape checks, and strict integer/numeric payload parsing. |
| `Client/request.py` | Added newline request termination and complete response reading. |
| `frontend/gateway.py` | Aligned command allowlist with server routes; validates request shapes/body size and treats TCP timeouts as errors. |
| `frontend/js/api.js` | Reports failed server logout instead of returning a success-shaped fallback. |
| `frontend/js/app.js` | Displays a warning when local logout succeeds but server logout cannot be confirmed. |
| `database/connection.py` | Reads host, port, user, password, and database from environment variables; default database name matches the schema. |
| `repositories/student_repository.py` | Replaced `SELECT *` student reads with public profile columns. |
| `repositories/result_repository.py` | Excludes NULL marks from result calculations and rankings. |
| `services/student_services.py` | Validates student names against the database column length. |
| `services/teacher_services.py` | Validates teacher-name length and finite, schema-range salaries. |
| `services/course_services.py` | Validates course-name length and finite, schema-range fees. |
| `services/result_services.py` | Rejects non-finite marks and handles NULL/empty result data safely. |
| `frontend/README.md` | Documents environment-based database configuration and corrects gateway/UI normalization notes. |
| `requirements.txt` | Declares MySQL Connector/Python and pytest. |
| `tests/test_gateway.py` | Adds gateway allowlist, malformed request, sanitization, and HTTP-to-TCP round-trip tests. |
| `tests/test_client_request.py` | Adds a large, chunked TCP response regression test. |
| `tests/test_server_protocol.py` | Adds split-request and invalid-ID parser tests with stubbed dependencies. |
| `tests/test_service_validation.py` | Adds isolated input-validation and NULL-result tests using stubbed repositories. |
| `NSMS_FUNCTIONALITY_AUDIT.md` | Adds this audit and verification report. |

No table, constraint, migration, or existing database record was changed.

## Tests and actual results

| Test/operation | Result |
| --- | --- |
| Pre-fix focused regression run | 4 failures reproduced: missing gateway routes, malformed request handling, and truncated CLI responses. |
| `python -m pytest -q tests\test_gateway.py tests\test_client_request.py tests\test_server_protocol.py tests\test_service_validation.py` | **12 passed**. These tests use local test servers or stubbed repositories and do not access MySQL. |
| Node syntax checks for `frontend/js/api.js` and `frontend/js/app.js` | **Passed**. |
| Node logout network-failure check | **Passed**: local clearing is safe and the failure response is not success-shaped. |
| Python compile check | **Passed** before the final NULL-handling edit; the final changed Python modules were also imported/executed by the passing focused tests. |
| `git diff --check` | **Passed**. |
| Actual gateway startup, alternate port 18080 | **Passed**: static UI returned HTTP 200; health endpoint reported TCP port 5000 reachable; unsupported command returned HTTP 400. The health probe confirms only TCP reachability, not the identity or database health of the listener on port 5000. |
| Actual `python server.py` startup | **Blocked**: MySQL rejected the connection because `NSMS_DB_PASSWORD` was not configured. |
| Full `python -m pytest -q` | **Blocked during collection**: seven database-backed test modules failed while importing the database connection (MySQL access denied). No feature tests ran and no rows were changed. |

At audit time, ports 3306, 5000, and 8080 already had listeners (`mysqld` and
Python processes). They were not stopped or modified. The gateway was tested on
18080 to avoid disrupting the existing process.

## Database issues and migration safety

- `database/schema.sql` defines `teacher_student_allocation` and
  `student_course_enrollment`, but the live database’s tables could not be
  inspected. `frontend/README.md` notes that the schema script includes a fixed
  `USE SCHOOL_NET`; do not run it wholesale against a production or differently
  named database.
- The database-backed tests create and delete random records, and import code
  connects to MySQL during test collection. They have no isolated-database
  fixture. Run them only against a disposable database with the required schema.
- No migration was executed. If `student_course_enrollment` or
  `teacher_student_allocation` is missing from an existing database, review the
  corresponding `CREATE TABLE IF NOT EXISTS` DDL and apply it only to the
  intended database after backup.
- `s_data.marks` is nullable and does not have a database-level range check.
  The service rejects values outside 0–100, but direct SQL writes can bypass
  that validation. Adding a `CHECK` constraint would require a separately
  reviewed migration and validation of existing rows; it was not done.
- `users.reference_id` has no foreign key to student/teacher records. Student
  deletion explicitly removes the student account, but teacher account cleanup
  and account-to-record referential integrity are not enforced by the schema.

## Missing features and remaining limitations

- Allocation updates are not implemented; only create/list/remove exist.
- There is no teacher-account provisioning flow or initial-admin bootstrap.
  Teacher/admin login therefore depends on accounts being provisioned outside
  the UI. Student credential setup is admin-only; self-service password change
  is not exposed as a server/gateway route.
- Student UI provides profile and calculated result views, not a detailed
  private marks-history or enrollment-management screen.
- Database CRUD, foreign-key behavior, real login/logout, authorization
  boundaries, result aggregations, and full E2E behavior still need testing on
  an isolated MySQL database.
- Existing processes occupy the default ports in this environment. Stop only
  the NSMS processes you own before starting replacements on 5000/8080.
- Removing the embedded credential from the current file does not erase it
  from prior commits. Rotate it; do not reuse it.

## Run instructions

1. From the repository root, install declared dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

2. Configure MySQL environment variables in the same PowerShell session that
   will start the server. Use a disposable database for tests:

   ```powershell
   $env:NSMS_DB_HOST = "localhost"
   $env:NSMS_DB_PORT = "3306"
   $env:NSMS_DB_USER = "root"
   $securePassword = Read-Host "MySQL password" -AsSecureString
   $passwordPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)
   try { $env:NSMS_DB_PASSWORD = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($passwordPointer) }
   finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($passwordPointer) }
   $env:NSMS_DB_NAME = "SCHOOL_NET"
   ```

   Set `NSMS_DB_NAME` to the disposable test database before running database
   tests. The schema file’s fixed `USE SCHOOL_NET` must be reviewed before
   applying any DDL. The default database name is `SCHOOL_NET`.
3. Ensure the selected database has the tables in `database/schema.sql`.
   Review its fixed database-selection statements before applying any DDL.
4. Start the TCP server:

   ```powershell
   python server.py
   ```

5. In a second PowerShell session, with any needed gateway overrides set, start
   the browser gateway:

   ```powershell
   python frontend\gateway.py
   ```

6. Open <http://127.0.0.1:8080>. If the default port is occupied, set
   `NSMS_GATEWAY_PORT` before starting the gateway.
7. Run the safe isolated regression suite:

   ```powershell
   python -m pytest -q tests\test_gateway.py tests\test_client_request.py tests\test_server_protocol.py tests\test_service_validation.py
   ```

8. Run the full suite only after selecting a disposable test database and
   verifying its schema:

   ```powershell
   python -m pytest -q
   ```
