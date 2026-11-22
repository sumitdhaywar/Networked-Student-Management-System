# NETWORKED STUDENT MANAGEMENT SYSTEM
## Complete Project Development Documentation

**Developer:** Sumit Dhaywar  
**Project:** Networked Student Management System (NSMS)  
**Programming Language:** Python  
**Database:** MySQL  
**Architecture:** Frontend → Gateway → Server → Database  
**Repository:** https://github.com/sumitdhaywar/Networked-Student-Management-System

---

# 1. PROJECT INTRODUCTION

The Networked Student Management System (NSMS) is a network-based academic management application developed using Python and MySQL.

The system is designed to centralize academic administration and manage student records, teacher information, courses, student allocations, marks, and examination results.

Unlike a basic single-user management application, NSMS uses a multi-layer client-server architecture. The frontend communicates through a dedicated gateway, which forwards requests to the backend server. The backend processes application operations and interacts with the MySQL database through its application and data-access components.

The project demonstrates practical implementation of:
- Python programming
- MySQL database management
- Client-server architecture
- Network communication
- CRUD operations
- Authentication
- Database relationships
- Backend application development

# 2. TECHNOLOGY STACK

| Component | Technology |
|---|---|
| Programming language | Python |
| Frontend | Python |
| Gateway | Python |
| Backend server | Python |
| Database | MySQL |
| Database language | SQL |
| Communication architecture | Client-server |
| Version control | Git and GitHub |

# 3. SYSTEM ARCHITECTURE

The confirmed high-level architecture is:

Frontend → Gateway → Server → Database

The backend implementation has also been discussed using service and repository components.

## Architecture responsibilities

### Frontend
- Provides the user interface.
- Accepts user inputs.
- Displays results.
- Provides access to management operations.

### Gateway
- Receives frontend requests.
- Handles communication between frontend and backend.
- Routes requests.
- Performs request validation and sanitization.

### Backend Server
- Receives requests from the gateway.
- Processes application operations.
- Coordinates backend functionality.
- Returns responses.

### Services
- Handle business logic.
- Coordinate student, teacher, course and marks operations.
- Apply application-level rules.

### Repositories
- Handle database operations.
- Execute SQL queries.
- Separate database access from business logic.

### MySQL Database
- Maintains centralized academic information.
- Stores user accounts.
- Maintains relationships between academic entities.

# 4. DATABASE DESIGN

The project uses MySQL.

## Main entities

1. Users
2. Students
3. Teachers
4. Courses
5. Teacher-student-course allocations
6. Marks and academic results

## Existing database records

The following records were present during the November 2026 testing session.

### Users
- admin01
- amit301
- adi101

### Students
- 101
- 103
- 104
- 105
- 5040

### Courses
- 201

### Teachers
- 301
- 302

These are existing development records, not credentials or a complete database schema.

## Teacher-student-course allocation

The project development notes identify an allocation relationship named:

`teacher_student_allocation`

Important fields:
- teacher_id
- student_id
- course_id

The allocation structure uses composite primary-key and foreign-key constraints.

The exact complete SQL schema should be taken from the actual MySQL database.

# 5. APPLICATION MODULES

## 5.1 Student Management

- Add student.
- Search student.
- List students.
- Update student.
- Delete student.

## 5.2 Teacher Management

- Add teacher.
- Maintain teacher records.
- Update teacher information.
- Display teacher information.
- Support allocation-related operations.

## 5.3 Course Management

- Add courses.
- Maintain course information.
- Manage course records.

## 5.4 Allocation Management

- Connect teachers with students and courses.
- Maintain allocation relationships.
- Use database constraints to preserve relationships.

## 5.5 Marks Management

- Enter marks.
- Associate marks with students.
- Associate marks with courses.
- Associate marks with teachers.
- Validate marks.

## 5.6 Result Management

- Calculate student results.
- Display results.
- Identify toppers.

## 5.7 Authentication

The project includes student login functionality and centralized account management.

Previous development discussions covered:
- User records.
- Password hashing.
- Authentication.
- Role-based permissions.
- Account-to-student/teacher reference mapping.

The earlier design preference was to keep separate login credentials limited to students rather than requiring separate teacher and administrator login accounts. The existing development database also contains admin01, amit301 and adi101; the exact current account-role configuration should be verified from the database.

# 6. SECURITY AND DATA VALIDATION

Previously discussed security improvements include:

- Password hashing using PBKDF2.
- Input validation.
- Gateway request sanitization.
- Database foreign-key constraints.
- Composite primary keys.
- Server-side permission checks.
- Keeping database credentials separate from public source code.

These should be verified against the current implementation before being described as completed security features.

# 7. DEVELOPMENT ENVIRONMENT

The project was developed and tested using Windows and PowerShell.

Earlier development directory:

`C:\Users\ADMIN\Desktop\networkedstudentmanagement`

Later testing directory:

`C:\Users\ADMIN\Desktop\networkedstudentmanagement_original`

The latest successful application launch instructions used the second directory.

## Starting the application

Open the project directory:

```powershell
cd "C:\Users\ADMIN\Desktop\networkedstudentmanagement_original"
```

### Terminal 1 – Backend Server

```powershell
python server.py
```

### Terminal 2 – Gateway

```powershell
cd "C:\Users\ADMIN\Desktop\networkedstudentmanagement_original"
python frontend\gateway.py
```

### Access the application

http://127.0.0.1:8080

If port 8080 is busy, the gateway can be started on another configured port:

```powershell
$env:NSMS_GATEWAY_PORT="8090"
python frontend\gateway.py
```

Then access:

http://127.0.0.1:8090

# 8. TESTING AND VERIFICATION HISTORY

The project was tested through application execution and previous testing workflows.

Previously recorded testing notes mentioned:

- 10 automated pytest tests passing.
- 23 out of 23 live gateway checks passing.

These are historical reported results and should be rerun against the current repository before being treated as final release results.

## Manual testing examples

Marks entry testing used:

| Field | Test value |
|---|---|
| Student ID | 101 |
| Course ID | 201 |
| Teacher ID | 301 |
| Marks | 0–100 |

Other functionality to verify:
- Login.
- Student CRUD operations.
- Teacher management.
- Course management.
- Allocation management.
- Marks entry.
- Result calculation.
- Topper identification.
- Gateway-server communication.
- Database connectivity.

# 9. PROJECT DESIGN DECISIONS

The following preferences were established during development:

1. Python is used for the application frontend and backend.
2. MySQL is the database.
3. The system follows Frontend → Gateway → Server → Database architecture.
4. Only students were intended to receive separate login credentials in the original design preference.
5. Teacher and course management should be integrated without breaking existing functionality.
6. Existing working code should be preserved when adding features.
7. New code should have comments identifying additions where appropriate.
8. The implementation should remain understandable and maintainable.
9. Avoid unnecessary complexity and excessive abstraction.
10. The project should be suitable for an academic demonstration and a GitHub portfolio.

# 10. GITHUB REPOSITORY

Repository:

https://github.com/sumitdhaywar/Networked-Student-Management-System

Repository name:

Networked-Student-Management-System

Developer:

Sumit Dhaywar

The README documentation has been prepared to explain:
- Project overview.
- Objectives.
- Architecture.
- Technology stack.
- Application modules.
- Database design.
- Installation.
- Testing.
- Security.
- Future improvements.

Recommended additional repository material:
- Actual system architecture diagram.
- MySQL ER diagram.
- Application screenshots.
- Database schema.
- Requirements file.
- Testing documentation.

# 11. FUTURE DEVELOPMENT

Potential improvements include:

- Improved dashboard.
- More comprehensive academic reports.
- Performance analytics.
- Better error handling.
- More automated testing.
- Database optimization.
- Improved documentation.
- Additional administrative functionality.

# 12. PROJECT STATUS

The project has reached a working application stage.

The latest recorded local test confirmed that:
- The backend server could be started.
- The gateway could be started separately.
- Chrome could access the application.
- The application was running successfully.

The OpenCode build process previously stopped at 51%, but the application was subsequently reported to be working.

The project has a GitHub repository and README preparation is underway.

The next important steps are:
1. Verify the actual repository structure.
2. Verify the complete MySQL schema.
3. Verify all modules against the running application.
4. Confirm testing results.
5. Add screenshots and architecture documentation.
6. Ensure the GitHub repository contains no sensitive information.

---

**END OF MASTER DEVELOPMENT RECORD**

This document consolidates the available NSMS development history and should be treated as the central project reference. Exact implementation details should always be checked against the current source code and MySQL database.
