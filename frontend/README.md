# NSMS Web Frontend (standalone)

A browser frontend for the **Networked Student Management System**. The UI lives
entirely inside this `frontend/` folder. The optional marks & analytics features
required a few **additive, backwards-compatible** additions outside this folder;
existing code paths were not changed (see "Server-side additions").

```
browser (index.html + js/css)
        |
        | HTTP + JSON
        v
frontend/gateway.py  (port 8080)   <-- new, lives only in this folder
        |
        | TCP + JSON (same protocol server.py already speaks)
        v
server.py            (port 5000)   <-- existing code + a few new request routes
        |
        v
services -> repositories -> MySQL
```

## Why the gateway is needed

Your `server.py` listens on a raw TCP socket. A browser cannot open a raw TCP
connection, so `gateway.py` is a tiny HTTP-to-TCP bridge. It accepts the exact
JSON your server already understands:

```json
{ "request": "Search_Student", "data": { "id": 101 }, "session_token": "..." }
```

Keep the two processes running side by side:

1. `python server.py` (your existing server, port 5000)
2. `python frontend/gateway.py` (this frontend, port 8080)
3. Open <http://127.0.0.1:8080>

The gateway only uses the Python standard library. Install the server and test
dependencies with `python -m pip install -r requirements.txt`.

## Database configuration

Configure database connection values in environment variables rather than
keeping a password in source:

| Variable | Default | Meaning |
| --- | --- | --- |
| `NSMS_DB_HOST` | `localhost` | MySQL host |
| `NSMS_DB_PORT` | `3306` | MySQL port |
| `NSMS_DB_USER` | `root` | MySQL user |
| `NSMS_DB_PASSWORD` | empty | MySQL password |
| `NSMS_DB_NAME` | `SCHOOL_NET` | Existing database name |

PowerShell example (the password is entered securely and kept in the current
terminal session):

```powershell
$env:NSMS_DB_HOST = "localhost"
$env:NSMS_DB_PORT = "3306"
$env:NSMS_DB_USER = "root"
$securePassword = Read-Host "MySQL password" -AsSecureString
$passwordPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)
try { $env:NSMS_DB_PASSWORD = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($passwordPointer) }
finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($passwordPointer) }
$env:NSMS_DB_NAME = "SCHOOL_NET"
python server.py
```

The server expects the tables in `database/schema.sql` to already exist. The
schema script contains a fixed `USE SCHOOL_NET`; do not run the whole script
when preparing a differently named test database. Select the disposable test
database and review the table DDL before applying it. Never apply schema SQL to
an existing database without a backup.

### Optional settings

| Variable | Default | Meaning |
| --- | --- | --- |
| `NSMS_SERVER_HOST` | `127.0.0.1` | address of your TCP server |
| `NSMS_SERVER_PORT` | `5000` | port of your TCP server |
| `NSMS_GATEWAY_HOST` | `127.0.0.1` | address the gateway binds to |
| `NSMS_GATEWAY_PORT` | `8080` | UI port |

Example (PowerShell):

```powershell
$env:NSMS_SERVER_PORT = "5000"
python frontend/gateway.py
```

## What the UI covers

| Role | Screens |
| --- | --- |
| **Admin** | Dashboard, student directory (add / search / edit / delete), teacher directory (add / search / edit / delete), student allocations (assign / list / remove), course directory (add / search / edit / delete), course enrollments (enroll / roster by course / remove), student login credentials, add marks, course-by-course toppers, class statistics, all marks records (edit / delete) |
| **Teacher** | Dashboard, student lookup, my allocated students, add marks (teacher ID locked to their session), course-by-course toppers, class statistics, own marks records (edit / delete; other teachers' records are view-only) |
| **Student** | Profile (own record), own result, course-by-course toppers |

Extra safety in the gateway: student rows are returned to the browser without the
`password_hash` column (`Search_Student` / `Display All Student`), and student
and topper tuples are normalized there. The UI maps result, teacher, course,
allocation, and enrollment tuples to display fields. The credential route
returns no password data.

## Server-side additions (additive only)

These routes back the marks & analytics screens. They reuse the existing
services/repositories and do not modify any existing behaviour:

| Layer | Addition |
| --- | --- |
| `server.py` | Requests `Display All Result`, `result_statistics`, `Update_Marks`, `Delete_Marks`, and `course_toppers`; teachers can only change marks records whose `teacher_id` matches their session `reference_id` |
| `services/result_services.py` | `get_result_statistics_se()` (class average, highest, lowest, passed, failed) and `get_course_toppers_se()` (independent course rankings) |
| `repositories/result_repository.py` | `get_result_statistics_rows()` and `get_course_topper_rows()` (average marks grouped and ranked separately per course) |
| `frontend/gateway.py` | Whitelists the requests and normalizes `Display All Result` rows |

Pass/fail is computed exactly like the existing `calculate_result_se()`: a student
passes when **every** mark is `>= 35`.

After updating these files, **restart `server.py` and `gateway.py`** so the new
routes and whitelist are loaded. The database schema and data are unchanged.
The dashboard loads a topper for each course automatically; courses without
marks remain visible with a "No marks recorded" message.

### Teacher, course and allocated-student additions

These routes reuse the existing teacher/course services and repositories, plus a
new allocation repository/service. All previous behaviour is unchanged.

| Layer | Addition |
| --- | --- |
| `server.py` | Teacher requests `Add_Teacher`, `Search_Teacher`, `Display All Teachers`, `Update_Teacher`, `Delete_Teacher` (admin); course requests `Add_Course`, `Search_Course`, `Display All Courses`, `Update_Course`, `Delete_Course` (admin); `Allocate_Student`, `Display All Allocations`, `Remove_Allocation` (admin); `View_My_Allocated_Students` (teacher, uses session `reference_id`); `Set_Student_Credentials` (admin) |
| `repositories/allocation_repository.py` | New file: add/get/list/delete rows joined with student, course and teacher names |
| `services/allocation_services.py` | New file: validation, existence checks, duplicate protection and friendly messages |
| `frontend/gateway.py` | Whitelists the new request names and normalizes teacher, course and allocation rows |
| `database/schema.sql` | Appended `teacher_student_allocation(teacher_id, student_id, course_id)` with foreign keys to `teacher`, `student` and `course` |
| `Client/menu.py` | Admin menu split into Student / Teacher / Course / Marks / Result / Student Login submenus; teacher menu gains "View My Allocated Students" |
| `frontend/js/app.js` | Teachers, Courses, Student logins and My students screens with modals, tables and allocation management |

Teachers can never request another teacher's allocations: `View_My_Allocated_Students`
ignores any client-supplied teacher ID and always uses the verified session
`reference_id`. Deleting a teacher/course that still has allocations is rejected
by the foreign key; remove the allocation first.

### Course enrollment rosters

Course enrollment is separate from teacher allocation and marks records. Admins
can enroll an existing student in a course, filter the roster by course, and
remove an enrollment without changing teacher assignments or marks.

| Layer | Addition |
| --- | --- |
| `database/schema.sql` | Adds `student_course_enrollment(student_id, course_id)` with a composite primary key and foreign keys |
| `repositories/enrollment_repository.py` / `services/enrollment_services.py` | Add, list and remove enrollments with ID validation, existence checks and duplicate protection |
| `server.py` | Adds the admin-only `Enroll_Student`, `Display All Enrollments` and `Remove_Enrollment` requests |
| `frontend/gateway.py` | Whitelists enrollment requests |
| `frontend/js/app.js` | Adds the admin course-enrollment screen and course-filtered roster |

For an existing database, run the new `CREATE TABLE IF NOT EXISTS
student_course_enrollment` statement from `database/schema.sql` once before using
the enrollment screen. Foreign keys prevent deleting a student or course that
still has enrollments; remove the affected enrollments first.

Deleting a student removes their marks, teacher allocations, course enrollments,
and linked student login in one transaction before deleting the student record.
The confirmation dialog lists these associated records.

Student Login Management creates or updates an account in the centralized
`users` table with `role = 'student'` and `reference_id` equal to the student ID.
It reuses the existing PBKDF2 `salt$hash` format, rejects usernames already used
by another account, and updates the same account instead of creating duplicates
for one student. The login path itself is unchanged.

## Files

```
frontend/
├── gateway.py        HTTP -> TCP bridge + static file server (stdlib only)
├── index.html        single-page shell
├── css/styles.css    all styling, responsive
├── js/api.js         gateway client + session token storage
├── js/app.js         UI, routing by role, forms, tables, toasts
└── README.md         this file
```

## Notes about changes to your existing files

Core screens (login, students, add marks, calculate result, topper) need no
changes outside `frontend/`. The optional analytics screens use the additive
routes listed above.

If you later wanted the browser to connect to the socket server *without* this
gateway, that would need changes on the server side (documented here only, not
applied):

- `server.py` would need to expose HTTP or WebSocket endpoints (for example with
  `http.server` or `websockets`) instead of a raw TCP socket.
- Each HTTP handler would reuse the same `auth_service` / `student_service` /
  `result_service` calls that already exist, so the business logic would not change.
- CORS headers and a static-file route would also be needed if the same process
  served this UI.

Until then, run `gateway.py` next to `server.py`.

## Troubleshooting

- **"Cannot reach the NSMS server"** - start `server.py` first; check the port.
- **"Login failed"** - the `users` table must contain a valid account whose
  `password_hash` uses the `salt$hash` PBKDF2 format expected by `auth_services.py`.
- **Port already in use** - change `NSMS_GATEWAY_PORT`.
- **Marks rejected** - the student, course, and teacher IDs must exist because the
  `s_data` table has foreign keys.
- **"Unsupported request" for stats / marks editing** - restart `gateway.py` and
  `server.py` so the new request names are loaded.
- **"Unsupported request" for teacher / course / allocation screens** - restart
  `gateway.py` and `server.py` after pulling these additions.
- **"Unsupported request" for course enrollments** - apply the enrollment table
  statement to the database, then restart `gateway.py` and `server.py`.
- **Cannot delete a teacher or course used by an allocation** - remove the
  allocation in the Teachers screen first (foreign-key protection).
- **Teacher cannot edit a record** - teachers may only change marks whose
  `teacher_id` equals their account's `reference_id`; admins can edit any record.
