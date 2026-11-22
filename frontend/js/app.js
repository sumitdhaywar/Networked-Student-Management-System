import * as api from "./api.js";

const app = document.getElementById("app");
const toastStack = document.getElementById("toast-stack");

const ICONS = {
  grid: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>',
  users: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.2"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 5.5a3 3 0 0 1 0 5.6"/><path d="M17.5 20a6.5 6.5 0 0 0-2.2-4.9"/></svg>',
  search: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/></svg>',
  edit: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>',
  chart: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20V10"/><path d="M10 20V4"/><path d="M16 20v-6"/><path d="M2 20h20"/></svg>',
  user: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="3.5"/><path d="M4.5 20a7.5 7.5 0 0 1 15 0"/></svg>',
  logout: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="m16 17 5-5-5-5"/><path d="M21 12H9"/></svg>',
  plus: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14"/><path d="M5 12h14"/></svg>',
  refresh: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-2.6-6.4"/><path d="M21 3v6h-6"/></svg>',
  check: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m4 12 5 5L20 6"/></svg>',
  alert: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 9v4"/><path d="M12 17h.01"/><path d="M10.3 3.9 2.6 17a2 2 0 0 0 1.7 3h15.4a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/></svg>',
  server: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="7" rx="2"/><rect x="3" y="13" width="18" height="7" rx="2"/><path d="M7 7.5h.01"/><path d="M7 16.5h.01"/></svg>',
  menu: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16"/><path d="M4 12h16"/><path d="M4 17h16"/></svg>',
  close: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 6l12 12"/><path d="M18 6 6 18"/></svg>',
  award: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="9" r="5"/><path d="m9 14-1.5 6 4.5-2.5L16.5 20 15 14"/></svg>',
  key: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="15" r="4"/><path d="m11 12 8-8"/><path d="m17 4 3 3"/><path d="m15 6 2 2"/></svg>',
  trash: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M6 7l1 13h10l1-13"/><path d="M9 7V4h6v3"/></svg>',
  arrow: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></svg>',
};

const NAV = {
  admin: [
    { id: "dashboard", label: "Dashboard", icon: "grid" },
    { id: "students", label: "Students", icon: "users" },
    // ===== ADDED: Teacher, Course and Student Login Management navigation =====
    { id: "teachers", label: "Teachers", icon: "award" },
    { id: "courses", label: "Courses", icon: "grid" },
    { id: "enrollments", label: "Enrollments", icon: "users" },
    { id: "logins", label: "Student logins", icon: "key" },
    { id: "marks", label: "Add marks", icon: "edit" },
    { id: "results", label: "Results", icon: "chart" },
  ],
  teacher: [
    { id: "dashboard", label: "Dashboard", icon: "grid" },
    { id: "students", label: "Student lookup", icon: "search" },
    // ===== ADDED: Teacher Allocated Students Feature - navigation =====
    { id: "allocated", label: "My students", icon: "users" },
    { id: "marks", label: "Add marks", icon: "edit" },
    { id: "results", label: "Results", icon: "chart" },
  ],
  student: [
    { id: "dashboard", label: "My profile", icon: "user" },
    { id: "results", label: "My result", icon: "chart" },
  ],
};

const state = {
  user: api.getUser(),
  view: "",
  students: [],
  // ===== ADDED: Teacher, Course and Allocated Student state =====
  teachers: [],
  courses: [],
  allocations: [],
  enrollments: [],
  enrollmentCourseFilter: "all",
  teacherSearch: null,
  courseSearch: null,
  courseToppers: [],
  courseToppersLoaded: false,
  courseToppersLoading: false,
  searchResult: null,
  profile: null,
  result: null,
  calcId: "",
  results: [],
  stats: null,
  health: null,
  sidebarOpen: false,
};

let modalOpen = false;

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (character) => {
    const map = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    };
    return map[character];
  });
}

function fmt(value) {
  const number = Number(value);
  if (!Number.isFinite(number)) return "\u2014";
  return number.toFixed(2).replace(/\.00$/, "");
}

function initials(name) {
  const parts = String(name || "")
    .trim()
    .split(/\s+/)
    .filter(Boolean);
  if (!parts.length) return "?";
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

function icon(name, className = "") {
  const markup = ICONS[name] || "";
  return `<span class="svg-icon ${className}">${markup}</span>`;
}

function roleLabel(role) {
  return String(role || "").charAt(0).toUpperCase() + String(role || "").slice(1);
}

function field(form, name) {
  return form.elements.namedItem(name);
}

function toStudent(raw) {
  if (!raw) return null;
  if (Array.isArray(raw)) {
    return {
      id: raw[0],
      name: raw[1],
      age: raw[2],
      user_name: raw[3] || "",
    };
  }
  return {
    id: raw.id,
    name: raw.name,
    age: raw.age,
    user_name: raw.user_name || raw.username || "",
  };
}

function toResult(raw) {
  if (!raw) return null;
  if (Array.isArray(raw)) {
    return {
      roll: raw[0],
      student_id: raw[1],
      course_id: raw[2],
      teacher_id: raw[3],
      marks: raw[4],
    };
  }
  return {
    roll: raw.roll,
    student_id: raw.student_id ?? raw.id,
    course_id: raw.course_id ?? raw.co_id,
    teacher_id: raw.teacher_id ?? raw.t_id,
    marks: raw.marks,
  };
}

// ===== ADDED: Teacher Management Feature - START =====
function toTeacher(raw) {
  if (!raw) return null;
  if (Array.isArray(raw)) {
    return {
      teacher_id: raw[0],
      teacher_name: raw[1],
      salary: raw[2],
      joining_date: raw[3],
    };
  }
  return {
    teacher_id: raw.teacher_id ?? raw.t_id,
    teacher_name: raw.teacher_name ?? raw.t_name,
    salary: raw.salary,
    joining_date: raw.joining_date ?? raw.j_o_d,
  };
}
// ===== ADDED: Teacher Management Feature - END =====

// ===== ADDED: Course Management Feature - START =====
function toCourse(raw) {
  if (!raw) return null;
  if (Array.isArray(raw)) {
    return { course_id: raw[0], course_name: raw[1], course_fees: raw[2] };
  }
  return {
    course_id: raw.course_id ?? raw.co_id,
    course_name: raw.course_name ?? raw.co_name,
    course_fees: raw.course_fees ?? raw.fees,
  };
}
// ===== ADDED: Course Management Feature - END =====

// ===== ADDED: Teacher Allocated Students Feature - START =====
function toAllocation(raw) {
  if (!raw) return null;
  if (Array.isArray(raw)) {
    return {
      student_id: raw[0],
      student_name: raw[1],
      course_id: raw[2],
      course_name: raw[3],
      teacher_id: raw[4],
      teacher_name: raw[5],
    };
  }
  return {
    student_id: raw.student_id,
    student_name: raw.student_name,
    course_id: raw.course_id,
    course_name: raw.course_name,
    teacher_id: raw.teacher_id,
    teacher_name: raw.teacher_name,
  };
}
// ===== ADDED: Teacher Allocated Students Feature - END =====

function toEnrollment(raw) {
  if (!raw) return null;
  if (Array.isArray(raw)) {
    return {
      student_id: raw[0],
      student_name: raw[1],
      course_id: raw[2],
      course_name: raw[3],
    };
  }
  return {
    student_id: raw.student_id,
    student_name: raw.student_name,
    course_id: raw.course_id,
    course_name: raw.course_name,
  };
}

function showToast(message, type = "info", timeout = 4200) {
  if (!toastStack) return;
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  const iconName = type === "success" ? "check" : type === "error" ? "alert" : "server";
  toast.innerHTML = `
    <span class="toast-icon">${icon(iconName)}</span>
    <span class="toast-message">${esc(message)}</span>
    <button class="toast-close" type="button" aria-label="Dismiss">${icon("close")}</button>`;
  toast.querySelector(".toast-close").addEventListener("click", () => removeToast(toast));
  toastStack.appendChild(toast);
  requestAnimationFrame(() => toast.classList.add("show"));
  window.setTimeout(() => removeToast(toast), timeout);
}

function removeToast(toast) {
  if (!toast || !toast.isConnected) return;
  toast.classList.remove("show");
  window.setTimeout(() => toast.remove(), 200);
}

function setFormBusy(form, busy) {
  if (!form) return;
  const button = form.querySelector('button[type="submit"]');
  if (!button) return;
  if (busy) {
    button.dataset.label = button.innerHTML;
    button.disabled = true;
    button.classList.add("busy");
    button.innerHTML = `<span class="spinner"></span> Working...`;
  } else {
    button.disabled = false;
    button.classList.remove("busy");
    if (button.dataset.label) button.innerHTML = button.dataset.label;
  }
}

function firstView() {
  const nav = NAV[state.user?.role] || NAV.student;
  return nav[0].id;
}

function serverStatusHTML(health) {
  if (!health) {
    return `<span class="dot pending"></span><div><strong>Checking server...</strong><small>Please wait</small></div>`;
  }
  const server = health.server || {};
  const reachable = Boolean(server.reachable);
  return `<span class="dot ${reachable ? "ok" : "bad"}"></span><div><strong>${reachable ? "Server online" : "Server offline"}</strong><small>${esc(server.host || "127.0.0.1")}:${esc(server.port || 5000)}</small></div>`;
}

function emptyState(title, text) {
  return `<div class="empty-state"><span class="empty-icon">${icon("server")}</span><h4>${esc(title)}</h4><p>${esc(text)}</p></div>`;
}

function statCard(label, value, iconName, hint) {
  return `
    <article class="stat-card">
      <span class="stat-icon">${icon(iconName)}</span>
      <div class="stat-body">
        <span class="stat-label">${esc(label)}</span>
        <strong class="stat-value">${esc(value)}</strong>
        <span class="stat-hint">${esc(hint)}</span>
      </div>
    </article>`;
}

function actionRow(title, text, iconName, attrs) {
  return `
    <button class="action-row" ${attrs}>
      <span class="action-icon">${icon(iconName)}</span>
      <span class="action-copy"><strong>${esc(title)}</strong><small>${esc(text)}</small></span>
      <span class="action-arrow">${icon("arrow")}</span>
    </button>`;
}

function profileDetails(student) {
  return `
    <div class="student-card">
      <div class="student-avatar">${esc(initials(student.name))}</div>
      <div class="student-main">
        <h4>${esc(student.name)}</h4>
        <p class="muted">Student #${esc(student.id)}</p>
      </div>
      <dl class="detail-list">
        <div><dt>Student ID</dt><dd class="mono">${esc(student.id)}</dd></div>
        <div><dt>Age</dt><dd>${esc(student.age)}</dd></div>
        <div><dt>Username</dt><dd>${student.user_name ? esc(student.user_name) : '<span class="muted">Not set</span>'}</dd></div>
      </dl>
    </div>`;
}

function studentCard(student) {
  return profileDetails(student);
}

function courseToppersDisplay() {
  if (!state.courseToppersLoaded && state.courseToppersLoading) {
    return emptyState("Finding course toppers", "Checking each course's latest marks.");
  }
  if (!state.courseToppers.length) {
    return emptyState(
      "No courses available",
      "Add courses to see a separate topper for each course."
    );
  }

  return `
    <div class="course-topper-grid">
      ${state.courseToppers
        .map((course) => {
          const topper = course.topper;
          if (!topper) {
            return `
              <article class="course-topper-card pending">
                <div class="course-topper-heading">
                  <span class="eyebrow">Course #${esc(course.course_id)}</span>
                  <h4>${esc(course.course_name)}</h4>
                </div>
                <p class="muted">No marks recorded for this course yet.</p>
              </article>`;
          }
          return `
            <article class="course-topper-card">
              <div class="course-topper-heading">
                <span class="eyebrow">Course #${esc(course.course_id)}</span>
                <h4>${esc(course.course_name)}</h4>
              </div>
              <div class="course-topper-student">
                <div class="topper-avatar">${esc(initials(topper.name))}</div>
                <div class="topper-main">
                  <span class="eyebrow">Course topper</span>
                  <strong>${esc(topper.name)}</strong>
                  <small class="muted">Student #${esc(topper.id)}</small>
                </div>
                <div class="topper-metrics">
                  <div><span>Average</span><strong>${fmt(topper.average)}%</strong></div>
                </div>
              </div>
            </article>`;
        })
        .join("")}
    </div>`;
}

function statsGrid(stats) {
  if (!stats) {
    return emptyState(
      "No statistics loaded",
      "Load class statistics to see averages, extremes and pass / fail counts."
    );
  }

  const highest = stats.highest || {};
  const lowest = stats.lowest || {};
  return `
    <div class="stat-grid five">
      ${statCard("Class average", `${fmt(stats.class_average)}%`, "chart", `${stats.students_with_results ?? 0} students with results`)}
      ${statCard("Highest", highest.name || "\u2014", "award", highest.name ? `${fmt(highest.average)}% average` : "no data")}
      ${statCard("Lowest", lowest.name || "\u2014", "user", lowest.name ? `${fmt(lowest.average)}% average` : "no data")}
      ${statCard("Passed", stats.passed ?? "\u2014", "check", "students passing every subject")}
      ${statCard("Failed", stats.failed ?? "\u2014", "alert", "students with marks below 35")}
    </div>`;
}

function resultsTable() {
  if (!state.results.length) {
    return emptyState(
      "No marks records",
      "Marks submitted through Add marks will appear here."
    );
  }

  const isTeacher = state.user.role === "teacher";
  const rows = state.results
    .slice()
    .sort((a, b) => Number(b.roll) - Number(a.roll))
    .map((record) => {
      const canManage =
        !isTeacher ||
        String(record.teacher_id) === String(state.user.reference_id);
      const actions = canManage
        ? `<td class="table-actions">
             <button class="icon-btn" title="Edit marks" data-action="edit-result" data-roll="${esc(record.roll)}">${icon("edit")}</button>
             <button class="icon-btn danger" title="Delete marks" data-action="delete-result" data-roll="${esc(record.roll)}">${icon("trash")}</button>
           </td>`
        : `<td class="table-actions"><span class="muted">View only</span></td>`;
      return `
        <tr>
          <td class="mono">#${esc(record.roll)}</td>
          <td>Student #${esc(record.student_id)}</td>
          <td>Course #${esc(record.course_id)}</td>
          <td>Teacher #${esc(record.teacher_id)}</td>
          <td><strong>${fmt(record.marks)}</strong></td>
          ${actions}
        </tr>`;
    })
    .join("");

  return `
    <div class="table-wrap">
      <table>
        <thead>
          <tr><th>Roll</th><th>Student</th><th>Course</th><th>Teacher</th><th>Marks</th><th class="th-actions">Actions</th></tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>
    </div>`;
}

function resultCard(result) {
  const pass = String(result.status).toLowerCase() === "pass";
  return `
    <div class="result-card ${pass ? "pass" : "fail"}">
      <div class="result-head">
        <span class="badge ${pass ? "success" : "danger"}">${pass ? "PASS" : "FAIL"}</span>
        <span class="muted">Student #${esc(result.studentId)}</span>
      </div>
      <div class="result-metrics">
        <div><span>Total marks</span><strong>${fmt(result.total)}</strong></div>
        <div><span>Percentage</span><strong>${fmt(result.percentage)}%</strong></div>
        <div><span>Status</span><strong>${esc(result.status)}</strong></div>
      </div>
    </div>`;
}

function studentsTable(limit) {
  if (!state.students.length) {
    return emptyState("No students yet", "Add your first student to get started.");
  }

  const rows = state.students
    .slice()
    .sort((a, b) => Number(b.id) - Number(a.id))
    .slice(0, limit || state.students.length)
    .map(
      (student) => `
      <tr>
        <td class="mono">#${esc(student.id)}</td>
        <td><strong>${esc(student.name)}</strong></td>
        <td>${esc(student.age)}</td>
        <td>${student.user_name ? esc(student.user_name) : '<span class="muted">\u2014</span>'}</td>
        <td class="table-actions">
          <button class="icon-btn" title="Edit student" data-action="edit-student" data-id="${esc(student.id)}">${icon("edit")}</button>
          <button class="icon-btn danger" title="Delete student" data-action="delete-student" data-id="${esc(student.id)}">${icon("trash")}</button>
        </td>
      </tr>`
    )
    .join("");

  return `
    <div class="table-wrap">
      <table>
        <thead>
          <tr><th>ID</th><th>Name</th><th>Age</th><th>Username</th><th class="th-actions">Actions</th></tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>
    </div>`;
}

function recentStudentsTable() {
  if (!state.students.length) {
    return emptyState("No students loaded", "Student records will appear here.");
  }
  const rows = state.students
    .slice()
    .sort((a, b) => Number(b.id) - Number(a.id))
    .slice(0, 5)
    .map(
      (student) => `
      <tr>
        <td class="mono">#${esc(student.id)}</td>
        <td><strong>${esc(student.name)}</strong></td>
        <td>${esc(student.age)}</td>
      </tr>`
    )
    .join("");
  return `
    <div class="table-wrap">
      <table>
        <thead><tr><th>ID</th><th>Name</th><th>Age</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>
    </div>`;
}

// ===== ADDED: Teacher Management Feature - START =====
function teachersTable() {
  if (!state.teachers.length) {
    return emptyState("No teachers yet", "Add your first teacher to get started.");
  }

  const rows = state.teachers
    .slice()
    .sort((a, b) => Number(b.teacher_id) - Number(a.teacher_id))
    .map(
      (teacher) => `
      <tr>
        <td class="mono">#${esc(teacher.teacher_id)}</td>
        <td><strong>${esc(teacher.teacher_name)}</strong></td>
        <td>${fmt(teacher.salary)}</td>
        <td>${esc(teacher.joining_date ?? "\u2014")}</td>
        <td class="table-actions">
          <button class="icon-btn" title="Edit teacher" data-action="edit-teacher" data-id="${esc(teacher.teacher_id)}">${icon("edit")}</button>
          <button class="icon-btn danger" title="Delete teacher" data-action="delete-teacher" data-id="${esc(teacher.teacher_id)}">${icon("trash")}</button>
        </td>
      </tr>`
    )
    .join("");

  return `
    <div class="table-wrap">
      <table>
        <thead>
          <tr><th>ID</th><th>Name</th><th>Salary</th><th>Joining date</th><th class="th-actions">Actions</th></tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>
    </div>`;
}

function teacherSearchCard() {
  const teacher = state.teacherSearch;
  if (!teacher) return "";
  return `
    <div class="search-result">
      <div class="search-result-head">
        <h4>Search result</h4>
        <button class="icon-btn" data-action="clear-teacher-search" title="Clear">${icon("close")}</button>
      </div>
      <div class="student-card">
        <div class="student-avatar">${esc(initials(teacher.teacher_name))}</div>
        <div class="student-main">
          <h4>${esc(teacher.teacher_name)}</h4>
          <p class="muted">Teacher #${esc(teacher.teacher_id)}</p>
        </div>
        <dl class="detail-list">
          <div><dt>Salary</dt><dd>${fmt(teacher.salary)}</dd></div>
          <div><dt>Joining date</dt><dd>${esc(teacher.joining_date ?? "\u2014")}</dd></div>
        </dl>
      </div>
    </div>`;
}
// ===== ADDED: Teacher Management Feature - END =====

// ===== ADDED: Course Management Feature - START =====
function coursesTable() {
  if (!state.courses.length) {
    return emptyState("No courses yet", "Add your first course to get started.");
  }

  const rows = state.courses
    .slice()
    .sort((a, b) => Number(b.course_id) - Number(a.course_id))
    .map(
      (course) => `
      <tr>
        <td class="mono">#${esc(course.course_id)}</td>
        <td><strong>${esc(course.course_name)}</strong></td>
        <td>${fmt(course.course_fees)}</td>
        <td class="table-actions">
          <button class="icon-btn" title="Edit course" data-action="edit-course" data-id="${esc(course.course_id)}">${icon("edit")}</button>
          <button class="icon-btn danger" title="Delete course" data-action="delete-course" data-id="${esc(course.course_id)}">${icon("trash")}</button>
        </td>
      </tr>`
    )
    .join("");

  return `
    <div class="table-wrap">
      <table>
        <thead>
          <tr><th>ID</th><th>Name</th><th>Fees</th><th class="th-actions">Actions</th></tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>
    </div>`;
}

function courseSearchCard() {
  const course = state.courseSearch;
  if (!course) return "";
  return `
    <div class="search-result">
      <div class="search-result-head">
        <h4>Search result</h4>
        <button class="icon-btn" data-action="clear-course-search" title="Clear">${icon("close")}</button>
      </div>
      <div class="student-card">
        <div class="student-avatar">${esc(initials(course.course_name))}</div>
        <div class="student-main">
          <h4>${esc(course.course_name)}</h4>
          <p class="muted">Course #${esc(course.course_id)}</p>
        </div>
        <dl class="detail-list">
          <div><dt>Fees</dt><dd>${fmt(course.course_fees)}</dd></div>
        </dl>
      </div>
    </div>`;
}
// ===== ADDED: Course Management Feature - END =====

// ===== ADDED: Teacher Allocated Students Feature - START =====
function allocationsTable({ showTeacher = true, removable = false } = {}) {
  if (!state.allocations.length) {
    return emptyState(
      "No allocations yet",
      "Assign a student to a teacher and course to see the allocation here."
    );
  }

  const rows = state.allocations
    .map((allocation) => {
      const teacherCell = showTeacher
        ? `<td>${esc(allocation.teacher_name)} <span class="muted">#${esc(allocation.teacher_id)}</span></td>`
        : "";
      const actionCell = removable
        ? `<td class="table-actions">
             <button class="icon-btn danger" title="Remove allocation" data-action="remove-allocation"
               data-teacher="${esc(allocation.teacher_id)}"
               data-student="${esc(allocation.student_id)}"
               data-course="${esc(allocation.course_id)}">${icon("trash")}</button>
           </td>`
        : "";
      return `
        <tr>
          <td class="mono">#${esc(allocation.student_id)}</td>
          <td><strong>${esc(allocation.student_name)}</strong></td>
          <td>${esc(allocation.course_name)} <span class="muted">#${esc(allocation.course_id)}</span></td>
          ${teacherCell}
          ${actionCell}
        </tr>`;
    })
    .join("");

  return `
    <div class="table-wrap">
      <table>
        <thead>
          <tr><th>Student</th><th>Name</th><th>Course</th>${showTeacher ? "<th>Teacher</th>" : ""}${removable ? '<th class="th-actions">Actions</th>' : ""}</tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>
    </div>`;
}
// ===== ADDED: Teacher Allocated Students Feature - END =====

function viewMeta() {
  const role = state.user?.role;
  const view = state.view;
  if (view === "dashboard") {
    if (role === "student") {
      return { title: "My profile", subtitle: "Your linked student record and quick actions" };
    }
    return { title: "Dashboard", subtitle: "Overview of students, marks and results" };
  }
  if (view === "students") {
    return role === "admin"
      ? { title: "Students", subtitle: "Create, search, update and delete student records" }
      : { title: "Student lookup", subtitle: "Search for a student by their ID" };
  }
  if (view === "marks") {
    return { title: "Marks entry", subtitle: "Attach marks to a student's course record" };
  }
  if (view === "results") {
    return role === "student"
      ? { title: "My result", subtitle: "Calculate your total, percentage and pass / fail status" }
      : { title: "Results", subtitle: "Calculate results, review marks records and class statistics" };
  }
  // ===== ADDED: Teacher Management Feature - page metadata =====
  if (view === "teachers") {
    return { title: "Teachers", subtitle: "Create, search, update and delete teachers; allocate students" };
  }
  // ===== ADDED: Course Management Feature - page metadata =====
  if (view === "courses") {
    return { title: "Courses", subtitle: "Create, search, update and delete courses" };
  }
  if (view === "enrollments") {
    return { title: "Course enrollments", subtitle: "Enroll students and manage course rosters" };
  }
  // ===== ADDED: Teacher Allocated Students Feature - page metadata =====
  if (view === "allocated") {
    return { title: "My students", subtitle: "Students allocated to your teacher account" };
  }
  // ===== ADDED: Student Login Management Feature - page metadata =====
  if (view === "logins") {
    return { title: "Student logins", subtitle: "Create or reset student credentials" };
  }
  return { title: "NSMS", subtitle: "" };
}

function adminDashboard() {
  const total = state.students.length;
  return `
    <div class="admin-dashboard">
      <section class="hero-card">
        <div class="hero-copy">
          <span class="eyebrow">Administrator workspace</span>
          <h2>Welcome back, ${esc(state.user.username)}</h2>
          <p>Manage student records, submit marks, and review performance across the whole network.</p>
        </div>
        <div class="hero-actions">
          <button class="btn primary" data-action="add-student">${icon("plus")} Add student</button>
          <button class="btn outline" data-nav="results">${icon("chart")} Review results</button>
        </div>
      </section>

      <div class="stat-grid">
        ${statCard("Total students", total ? total : "\u2014", "users", "records loaded")}
        ${statCard("Course toppers", state.courseToppers.filter((course) => course.topper).length || "\u2014", "award", `${state.courseToppers.length} courses ranked`)}
        ${statCard("Role", roleLabel(state.user.role), "user", "full system access")}
        ${statCard("Session", "Active", "key", "expires after 30 minutes")}
      </div>

      <div class="grid two admin-overview-grid">
        <section class="card">
          <div class="card-head">
            <div><h3>Recent students</h3><p>Latest records in the directory</p></div>
            <button class="btn ghost sm" data-nav="students">View all ${icon("arrow")}</button>
          </div>
          ${recentStudentsTable()}
        </section>
        <section class="card">
          <div class="card-head">
            <div><h3>Top student in each course</h3><p>Each course is ranked independently by average marks</p></div>
            <button class="btn ghost sm" data-action="load-topper" ${state.courseToppersLoading ? "disabled" : ""} aria-busy="${state.courseToppersLoading}">
              ${icon("refresh")} ${state.courseToppersLoading ? "Loading" : "Refresh"}
            </button>
          </div>
          <div class="admin-topper">${courseToppersDisplay()}</div>
          <div class="quick-actions">
            <div class="card-head">
              <div><h3>Quick actions</h3><p>Jump straight to a task</p></div>
            </div>
            <div class="action-list">
              ${actionRow("Add a new student", "Create a record in the database", "plus", 'data-action="add-student"')}
              ${actionRow("Submit marks", "Record a score for a course", "edit", 'data-nav="marks"')}
              ${actionRow("Search a student", "Look up a student by ID", "search", 'data-nav="students"')}
            </div>
          </div>
        </section>
      </div>
    </div>`;
}

function teacherDashboard() {
  return `
    <section class="hero-card teacher">
      <div class="hero-copy">
        <span class="eyebrow">Teacher workspace</span>
        <h2>Welcome, ${esc(state.user.username)}</h2>
        <p>Look up students, submit marks for your courses, and review results.</p>
      </div>
      <div class="hero-actions">
        <button class="btn primary" data-nav="marks">${icon("edit")} Add marks</button>
        <button class="btn outline" data-nav="students">${icon("search")} Find student</button>
        <!-- ===== ADDED: Teacher Allocated Students Feature - shortcut ===== -->
        <button class="btn outline" data-nav="allocated">${icon("users")} My students</button>
      </div>
    </section>

    <div class="grid two">
      <section class="card">
        <div class="card-head">
          <div><h3>Quick student lookup</h3><p>Search a student by ID</p></div>
        </div>
        <form class="search-row" data-form="search-student">
          <div class="search-box">${icon("search")}<input name="id" type="number" min="1" required placeholder="Student ID"></div>
          <button class="btn primary" type="submit">Search</button>
        </form>
        <div class="search-result-inline">
          ${state.searchResult ? studentCard(state.searchResult) : emptyState("No student selected", "Enter a student ID above to view their record.")}
        </div>
      </section>

      <section class="card">
        <div class="card-head">
          <div><h3>Course toppers</h3><p>Highest average in each course</p></div>
          <button class="btn ghost sm" data-action="load-topper">${icon("refresh")} Refresh</button>
        </div>
        ${courseToppersDisplay()}
      </section>
    </div>`;
}

function studentDashboard() {
  const profile = state.profile;
  return `
    <section class="hero-card student">
      <div class="hero-copy">
        <span class="eyebrow">Student portal</span>
        <h2>Hello, ${esc(profile ? profile.name : state.user.username)}</h2>
        <p>View your profile, calculate your result, and see who is leading the class.</p>
      </div>
      <div class="hero-actions">
        <button class="btn primary" data-nav="results">${icon("chart")} My result</button>
        <button class="btn outline" data-action="refresh-profile">${icon("refresh")} Refresh</button>
      </div>
    </section>

    <div class="grid two">
      <section class="card">
        <div class="card-head"><div><h3>My profile</h3><p>Linked student record</p></div></div>
        ${profile ? profileDetails(profile) : emptyState("Profile not available", "Your account may not be linked to a student record. Contact an administrator.")}
      </section>
      <section class="card">
        <div class="card-head">
          <div><h3>Course toppers</h3><p>Highest average in each course</p></div>
          <button class="btn ghost sm" data-action="load-topper">${icon("refresh")} Refresh</button>
        </div>
        ${courseToppersDisplay()}
      </section>
    </div>`;
}

function studentsView() {
  const isAdmin = state.user.role === "admin";

  if (!isAdmin) {
    return `
      <section class="card narrow">
        <div class="card-head">
          <div><h3>Student lookup</h3><p>Search a student by ID to view their record</p></div>
        </div>
        <form class="search-row" data-form="search-student">
          <div class="search-box">${icon("search")}<input name="id" type="number" min="1" required placeholder="Student ID"></div>
          <button class="btn primary" type="submit">Search</button>
          <button class="btn ghost" type="button" data-action="clear-search">Clear</button>
        </form>
        <div class="search-result-inline">
          ${state.searchResult ? studentCard(state.searchResult) : emptyState("No student selected", "Enter a student ID above to view their record.")}
        </div>
      </section>`;
  }

  return `
    <section class="card">
      <div class="card-head">
        <div><h3>Student directory</h3><p>All records from the server</p></div>
        <div class="row gap">
          <button class="btn outline sm" data-action="refresh-students">${icon("refresh")} Refresh</button>
          <button class="btn primary sm" data-action="add-student">${icon("plus")} Add student</button>
        </div>
      </div>

      <form class="search-row" data-form="search-student">
        <div class="search-box">${icon("search")}<input name="id" type="number" min="1" required placeholder="Search by student ID"></div>
        <button class="btn primary" type="submit">Search</button>
        <button class="btn ghost" type="button" data-action="clear-search">Clear</button>
      </form>

      ${
        state.searchResult
          ? `<div class="search-result">
              <div class="search-result-head">
                <h4>Search result</h4>
                <button class="icon-btn" data-action="clear-search" title="Clear">${icon("close")}</button>
              </div>
              ${studentCard(state.searchResult)}
            </div>`
          : ""
      }

      ${studentsTable()}
    </section>`;
}

function marksView() {
  const isTeacher = state.user.role === "teacher";
  const teacherId = isTeacher ? state.user.reference_id ?? "" : "";
  return `
    <div class="grid two">
      <section class="card">
        <div class="card-head">
          <div><h3>Submit marks</h3><p>Record a score for a student in a course</p></div>
        </div>
        <form class="form-grid" data-form="add-marks">
          <div class="field">
            <label for="mark-student">Student ID</label>
            <input id="mark-student" name="id" type="number" min="1" required placeholder="e.g. 101">
          </div>
          <div class="field">
            <label for="mark-course">Course ID</label>
            <input id="mark-course" name="co_id" type="number" min="1" required placeholder="e.g. 1">
          </div>
          <div class="field">
            <label for="mark-teacher">Teacher ID</label>
            <input id="mark-teacher" name="t_id" type="number" min="1" required value="${esc(teacherId)}" ${isTeacher ? "readonly" : ""} placeholder="e.g. 1">
          </div>
          <div class="field">
            <label for="mark-value">Marks (0 - 100)</label>
            <input id="mark-value" name="marks" type="number" min="0" max="100" step="0.01" required placeholder="e.g. 85">
          </div>
          <div class="form-actions">
            <button class="btn primary" type="submit">${icon("check")} Save marks</button>
          </div>
        </form>
      </section>

      <section class="card">
        <div class="card-head">
          <div><h3>Before you submit</h3><p>Marks are stored against existing records</p></div>
        </div>
        <ul class="tips">
          <li>The student, course and teacher IDs must already exist in the database.</li>
          <li>Marks must be a number between 0 and 100.</li>
          <li>${isTeacher ? `Your teacher ID is locked to <strong>${esc(teacherId)}</strong>.` : "Administrators can submit marks on behalf of any teacher."}</li>
          <li>Use the <strong>Results</strong> page to calculate totals and percentages.</li>
        </ul>
      </section>
    </div>`;
}

function resultsView() {
  const isStudent = state.user.role === "student";
  const defaultId = isStudent ? state.user.reference_id ?? "" : state.calcId || "";
  const recordsHint =
    state.user.role === "teacher"
      ? "Edit or delete your own marks record"
      : "Edit or delete any marks record";
  const staffExtras = isStudent
    ? ""
    : `
    <section class="card">
      <div class="card-head">
        <div><h3>Class statistics</h3><p>Average marks, extremes and pass / fail counts</p></div>
        <button class="btn ghost sm" data-action="load-stats">${icon("refresh")} Refresh</button>
      </div>
      ${statsGrid(state.stats)}
    </section>

    <section class="card">
      <div class="card-head">
        <div><h3>Marks records</h3><p>${esc(recordsHint)}</p></div>
        <button class="btn outline sm" data-action="refresh-results">${icon("refresh")} Refresh</button>
      </div>
      ${resultsTable()}
    </section>`;

  return `
    <div class="grid two">
      <section class="card">
        <div class="card-head">
          <div><h3>Calculate result</h3><p>Total, percentage and pass / fail status</p></div>
        </div>
        <form class="search-row" data-form="calculate-result">
          <div class="search-box">${icon("user")}<input name="id" type="number" min="1" required placeholder="Student ID" value="${esc(defaultId)}" ${isStudent ? "readonly" : ""}></div>
          <button class="btn primary" type="submit">Calculate</button>
        </form>
        <div class="result-output">
          ${state.result ? resultCard(state.result) : emptyState("No result yet", "Calculate a result to see total, percentage and status.")}
        </div>
      </section>

      <section class="card">
        <div class="card-head">
          <div><h3>Course toppers</h3><p>Ranked by average marks in each course</p></div>
          <button class="btn ghost sm" data-action="load-topper">${icon("refresh")} Load</button>
        </div>
        ${courseToppersDisplay()}
      </section>
    </div>${staffExtras}`;
}

// ===== ADDED: Teacher Management Feature - START =====
function teachersView() {
  return `
    <section class="card">
      <div class="card-head">
        <div><h3>Teacher directory</h3><p>All teacher records from the server</p></div>
        <div class="row gap">
          <button class="btn outline sm" data-action="refresh-teachers">${icon("refresh")} Refresh</button>
          <button class="btn primary sm" data-action="add-teacher">${icon("plus")} Add teacher</button>
        </div>
      </div>

      <form class="search-row" data-form="search-teacher">
        <div class="search-box">${icon("search")}<input name="t_id" type="number" min="1" required placeholder="Search by teacher ID"></div>
        <button class="btn primary" type="submit">Search</button>
        <button class="btn ghost" type="button" data-action="clear-teacher-search">Clear</button>
      </form>

      ${teacherSearchCard()}
      ${teachersTable()}
    </section>

    <section class="card">
      <div class="card-head">
        <div><h3>Student allocations</h3><p>Assign a student to a teacher and course</p></div>
        <button class="btn outline sm" data-action="refresh-allocations">${icon("refresh")} Refresh</button>
      </div>

      <form class="form-grid" data-form="allocate-student">
        <div class="field">
          <label for="alloc-teacher">Teacher ID</label>
          <input id="alloc-teacher" name="teacher_id" type="number" min="1" required placeholder="e.g. 301">
        </div>
        <div class="field">
          <label for="alloc-student">Student ID</label>
          <input id="alloc-student" name="student_id" type="number" min="1" required placeholder="e.g. 101">
        </div>
        <div class="field">
          <label for="alloc-course">Course ID</label>
          <input id="alloc-course" name="course_id" type="number" min="1" required placeholder="e.g. 201">
        </div>
        <div class="form-actions">
          <button class="btn primary" type="submit">${icon("plus")} Allocate student</button>
        </div>
      </form>

      ${allocationsTable({ showTeacher: true, removable: true })}
    </section>`;
}
// ===== ADDED: Teacher Management Feature - END =====

// ===== ADDED: Course Management Feature - START =====
function coursesView() {
  return `
    <section class="card">
      <div class="card-head">
        <div><h3>Course directory</h3><p>All course records from the server</p></div>
        <div class="row gap">
          <button class="btn outline sm" data-action="refresh-courses">${icon("refresh")} Refresh</button>
          <button class="btn primary sm" data-action="add-course">${icon("plus")} Add course</button>
        </div>
      </div>

      <form class="search-row" data-form="search-course">
        <div class="search-box">${icon("search")}<input name="co_id" type="number" min="1" required placeholder="Search by course ID"></div>
        <button class="btn primary" type="submit">Search</button>
        <button class="btn ghost" type="button" data-action="clear-course-search">Clear</button>
      </form>

      ${courseSearchCard()}
      ${coursesTable()}
    </section>`;
}
// ===== ADDED: Course Management Feature - END =====

function enrollmentOptions(items, idKey, nameKey) {
  if (!items.length) return "";
  return items
    .slice()
    .sort((a, b) => Number(a[idKey]) - Number(b[idKey]))
    .map(
      (item) =>
        `<option value="${esc(item[idKey])}">#${esc(item[idKey])} - ${esc(item[nameKey])}</option>`
    )
    .join("");
}

function enrollmentsTable() {
  const enrollments = state.enrollments.filter(
    (item) =>
      state.enrollmentCourseFilter === "all" ||
      String(item.course_id) === String(state.enrollmentCourseFilter)
  );
  if (!enrollments.length) {
    return emptyState(
      state.enrollmentCourseFilter === "all" ? "No course enrollments yet" : "No students in this course",
      "Enroll an existing student in a course to build its roster."
    );
  }

  const rows = enrollments
    .map(
      (enrollment) => `
        <tr>
          <td class="mono">#${esc(enrollment.student_id)}</td>
          <td><strong>${esc(enrollment.student_name)}</strong></td>
          <td>${esc(enrollment.course_name)} <span class="muted">#${esc(enrollment.course_id)}</span></td>
          <td class="table-actions">
            <button class="icon-btn danger" title="Remove course enrollment"
              data-action="remove-enrollment"
              data-student="${esc(enrollment.student_id)}"
              data-course="${esc(enrollment.course_id)}">${icon("trash")}</button>
          </td>
        </tr>`
    )
    .join("");

  return `
    <div class="table-wrap">
      <table>
        <thead><tr><th>Student ID</th><th>Student</th><th>Course</th><th class="th-actions">Actions</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>
    </div>`;
}

function enrollmentsView() {
  const courseOptions = state.courses
    .slice()
    .sort((a, b) => Number(a.course_id) - Number(b.course_id))
    .map(
      (course) =>
        `<option value="${esc(course.course_id)}" ${String(course.course_id) === String(state.enrollmentCourseFilter) ? "selected" : ""}>${esc(course.course_name)} (#${esc(course.course_id)})</option>`
    )
    .join("");
  const studentsReady = state.students.length > 0;
  const coursesReady = state.courses.length > 0;

  return `
    <section class="card">
      <div class="card-head">
        <div><h3>Enroll student in a course</h3><p>This course roster is separate from teacher allocation and marks entry.</p></div>
        <button class="btn outline sm" data-action="refresh-enrollments">${icon("refresh")} Refresh roster</button>
      </div>
      <form class="form-grid" data-form="enroll-student">
        <div class="field">
          <label for="enrollment-student">Student</label>
          <select id="enrollment-student" name="student_id" required ${studentsReady ? "" : "disabled"}>
            <option value="">${studentsReady ? "Select a student" : "Add a student first"}</option>
            ${enrollmentOptions(state.students, "id", "name")}
          </select>
        </div>
        <div class="field">
          <label for="enrollment-course">Course</label>
          <select id="enrollment-course" name="course_id" required ${coursesReady ? "" : "disabled"}>
            <option value="">${coursesReady ? "Select a course" : "Add a course first"}</option>
            ${enrollmentOptions(state.courses, "course_id", "course_name")}
          </select>
        </div>
        <div class="form-actions">
          <button class="btn primary" type="submit" ${studentsReady && coursesReady ? "" : "disabled"}>${icon("plus")} Enroll student</button>
        </div>
      </form>
    </section>

    <section class="card">
      <div class="card-head">
        <div><h3>Course roster</h3><p>${state.enrollments.length} enrollment${state.enrollments.length === 1 ? "" : "s"} across all courses</p></div>
        <label class="enrollment-filter-label" for="enrollment-course-filter">Show course
          <select id="enrollment-course-filter" data-enrollment-course-filter>
            <option value="all" ${state.enrollmentCourseFilter === "all" ? "selected" : ""}>All courses</option>
            ${courseOptions}
          </select>
        </label>
      </div>
      ${enrollmentsTable()}
    </section>`;
}

// ===== ADDED: Teacher Allocated Students Feature - START =====
function allocatedView() {
  return `
    <section class="card">
      <div class="card-head">
        <div><h3>My allocated students</h3><p>Students assigned to you by an administrator</p></div>
        <button class="btn outline sm" data-action="refresh-my-allocations">${icon("refresh")} Refresh</button>
      </div>
      ${allocationsTable({ showTeacher: false, removable: false })}
    </section>`;
}
// ===== ADDED: Teacher Allocated Students Feature - END =====

// ===== ADDED: Student Login Management Feature - START =====
function loginsView() {
  return `
    <section class="card narrow">
      <div class="card-head">
        <div><h3>Set student credentials</h3><p>Create or reset the login for an existing student</p></div>
      </div>
      <form class="form-grid" data-form="set-credentials">
        <div class="field">
          <label for="login-student">Student ID</label>
          <input id="login-student" name="id" type="number" min="1" required placeholder="e.g. 101">
        </div>
        <div class="field">
          <label for="login-username-new">Username</label>
            <input id="login-username-new" name="user_name" required maxlength="20" placeholder="e.g. adi101">
        </div>
        <div class="field">
          <label for="login-password-new">Password</label>
          <input id="login-password-new" name="password" type="password" autocomplete="new-password" required minlength="8" placeholder="At least 8 characters">
        </div>
        <div class="form-actions">
          <button class="btn primary" type="submit">${icon("key")} Save credentials</button>
        </div>
      </form>
      <!-- ===== UPDATED: Existing Code - Student credentials are stored in the users table ===== -->
      <ul class="tips">
        <li>Credentials are stored in the centralized users table with the student role.</li>
        <li>Passwords are hashed before they are stored; they are never shown again.</li>
        <li>The username must be unique across all user accounts.</li>
      </ul>
    </section>`;
}
// ===== ADDED: Student Login Management Feature - END =====

function renderView() {
  switch (state.view) {
    case "dashboard":
      if (state.user.role === "admin") return adminDashboard();
      if (state.user.role === "teacher") return teacherDashboard();
      return studentDashboard();
    case "students":
      return studentsView();
    // ===== ADDED: Teacher, Course, Allocated and Login views =====
    case "teachers":
      return teachersView();
    case "courses":
      return coursesView();
    case "enrollments":
      return enrollmentsView();
    case "allocated":
      return allocatedView();
    case "logins":
      return loginsView();
    case "marks":
      return marksView();
    case "results":
      return resultsView();
    default:
      return "";
  }
}

function renderApp() {
  if (!state.user) {
    renderLogin();
    return;
  }

  const role = state.user.role;
  const nav = NAV[role] || NAV.student;
  if (!state.view || !nav.some((item) => item.id === state.view)) {
    state.view = firstView();
  }

  const meta = viewMeta();
  const navMarkup = nav
    .map(
      (item) => `
      <button class="nav-item ${state.view === item.id ? "active" : ""}" data-nav="${item.id}">
        <span class="nav-icon">${icon(item.icon)}</span>
        <span>${esc(item.label)}</span>
      </button>`
    )
    .join("");

  app.innerHTML = `
    <div class="app-shell">
      <div class="sidebar-backdrop ${state.sidebarOpen ? "show" : ""}" data-action="close-sidebar"></div>
      <aside class="sidebar ${state.sidebarOpen ? "open" : ""}">
        <div class="brand light">
          <span class="brand-mark">N</span>
          <div><strong>NSMS</strong><small>Student Management</small></div>
        </div>
        <nav class="nav">${navMarkup}</nav>
        <div class="sidebar-footer">
          <div class="server-status" data-role="server-status">${serverStatusHTML(state.health)}</div>
          <p class="sidebar-note">Connected to your TCP server through the standalone gateway.</p>
        </div>
      </aside>

      <div class="workspace">
        <header class="topbar">
          <button class="icon-btn menu-toggle" data-action="toggle-sidebar" title="Open navigation">${icon("menu")}</button>
          <div class="page-heading">
            <h1>${esc(meta.title)}</h1>
            <p>${esc(meta.subtitle)}</p>
          </div>
          <div class="topbar-right">
            <span class="pill role-pill ${esc(role)}">${esc(roleLabel(role))}</span>
            <div class="user-chip">
              <span class="avatar">${esc(initials(state.user.username))}</span>
              <div class="user-chip-copy"><strong>${esc(state.user.username)}</strong><small>${esc(roleLabel(role))}</small></div>
            </div>
            <button class="btn ghost sm logout-btn" data-action="logout">${icon("logout")}<span class="btn-label">Logout</span></button>
          </div>
        </header>

        <main class="view">${renderView()}</main>
      </div>
    </div>`;
}

function renderLogin() {
  app.innerHTML = `
    <div class="auth">
      <section class="auth-hero">
        <div class="brand light">
          <span class="brand-mark">N</span>
          <div><strong>NSMS</strong><small>Networked Student Management</small></div>
        </div>

        <div class="auth-copy">
          <span class="eyebrow light">Client &bull; Server &bull; Database</span>
          <h1>One console for your entire student network.</h1>
          <p>Connect to the NSMS socket server to manage students, submit marks, and review results from a single interface.</p>
          <ul class="feature-list">
            <li>${icon("users")}<div><strong>Student records</strong><span>Create, search, update and remove students.</span></div></li>
            <li>${icon("edit")}<div><strong>Marks entry</strong><span>Record scores against courses and teachers.</span></div></li>
            <li>${icon("chart")}<div><strong>Result analysis</strong><span>Totals, percentages, pass status and the topper.</span></div></li>
            <li>${icon("key")}<div><strong>Role-based access</strong><span>Separate admin, teacher and student workspaces.</span></div></li>
          </ul>
        </div>

        <p class="auth-foot">Frontend gateway talks to your existing TCP server &mdash; no changes required.</p>
      </section>

      <section class="auth-panel">
        <form class="auth-card" data-form="login">
          <div class="auth-card-head">
            <span class="badge primary">Secure sign in</span>
            <h2>Welcome back</h2>
            <p>Use the credentials stored in your <code>users</code> table.</p>
          </div>

          <div class="field">
            <label for="login-username">Username</label>
            <div class="input-icon">${icon("user")}<input id="login-username" name="username" autocomplete="username" required placeholder="admin"></div>
          </div>

          <div class="field">
            <label for="login-password">Password</label>
            <div class="input-icon">${icon("key")}<input id="login-password" name="password" type="password" autocomplete="current-password" required placeholder="Enter your password"></div>
          </div>

          <button class="btn primary block" type="submit">Sign in ${icon("arrow")}</button>

          <div class="server-status auth-status" data-role="server-status">${serverStatusHTML(state.health)}</div>
          <p class="auth-hint">Make sure <code>server.py</code> is running on port 5000 and the gateway on port 8080.</p>
        </form>
      </section>
    </div>`;
}

function enterView(view) {
  const nav = NAV[state.user?.role] || NAV.student;
  if (!nav.some((item) => item.id === view)) return;

  state.view = view;
  state.sidebarOpen = false;
  state.searchResult = view === "students" ? state.searchResult : null;
  // ===== ADDED: Keep teacher and course search results scoped to their views =====
  state.teacherSearch = view === "teachers" ? state.teacherSearch : null;
  state.courseSearch = view === "courses" ? state.courseSearch : null;

  renderApp();
  window.scrollTo({ top: 0, behavior: "smooth" });

  if (view === "dashboard") {
    if (state.user.role === "student" && !state.profile) loadProfile({ silent: true });
    if (state.user.role === "admin" && !state.students.length) loadStudents({ silent: true });
    if (!state.courseToppersLoaded) loadCourseToppers({ silent: true });
  }

  if (view === "students" && state.user.role === "admin" && !state.students.length) {
    loadStudents({ silent: true });
  }

  if (view === "results" && state.user.role !== "student") {
    loadResultsAndStats({ silent: true });
  }
  if (view === "results" && !state.courseToppersLoaded) {
    loadCourseToppers({ silent: true });
  }

  // ===== ADDED: Teacher, Course and Allocation view loading =====
  if (view === "teachers") {
    if (!state.teachers.length) loadTeachers({ silent: true });
    loadAllocations({ silent: true });
  }
  if (view === "courses" && !state.courses.length) {
    loadCourses({ silent: true });
  }
  if (view === "enrollments") {
    if (!state.students.length) loadStudents({ silent: true });
    if (!state.courses.length) loadCourses({ silent: true });
    loadEnrollments({ silent: true });
  }
  if (view === "allocated") {
    loadMyAllocations({ silent: true });
  }
}

async function syncHealth() {
  const payload = await api.health();
  state.health = payload;
  document
    .querySelectorAll('[data-role="server-status"]')
    .forEach((node) => {
      node.innerHTML = serverStatusHTML(state.health);
    });
}

async function handleLogin(form) {
  const username = String(field(form, "username").value || "").trim();
  const password = String(field(form, "password").value || "");

  if (!username || !password) {
    showToast("Enter your username and password.", "warning");
    return;
  }

  setFormBusy(form, true);
  try {
    const payload = await api.login(username, password);
    if (!payload.success) {
      showToast(payload.message || "Login failed.", "error");
      return;
    }

    state.user = api.getUser();
    state.view = firstView();
    state.students = [];
    // ===== ADDED: Reset teacher, course and allocation state on login =====
    state.teachers = [];
    state.courses = [];
    state.allocations = [];
    state.enrollments = [];
    state.enrollmentCourseFilter = "all";
    state.teacherSearch = null;
    state.courseSearch = null;
    state.courseToppers = [];
    state.courseToppersLoaded = false;
    state.courseToppersLoading = false;
    state.searchResult = null;
    state.profile = null;
    state.result = null;
    state.calcId = "";
    state.results = [];
    state.stats = null;
    state.sidebarOpen = false;

    showToast(`Welcome, ${state.user.username}.`, "success");
    renderApp();
    syncHealth();

    if (state.user.role === "admin") {
      loadStudents({ silent: true });
    }
    loadCourseToppers({ silent: true });
    if (state.user.role === "student") loadProfile({ silent: true });
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    setFormBusy(form, false);
  }
}

async function handleLogout() {
  await api.logout();
  state.user = null;
  state.view = "";
  state.students = [];
  // ===== ADDED: Reset teacher, course and allocation state on logout =====
  state.teachers = [];
  state.courses = [];
  state.allocations = [];
  state.enrollments = [];
  state.enrollmentCourseFilter = "all";
  state.teacherSearch = null;
  state.courseSearch = null;
  state.courseToppers = [];
  state.courseToppersLoaded = false;
  state.courseToppersLoading = false;
  state.searchResult = null;
  state.profile = null;
  state.result = null;
  state.calcId = "";
  state.results = [];
  state.stats = null;
  state.sidebarOpen = false;
  renderLogin();
  syncHealth();
  showToast("You have been logged out.", "info");
}

async function loadStudents({ silent = false } = {}) {
  try {
    const payload = await api.command("Display All Student");
    if (!payload.success) {
      if (!silent) showToast(payload.message || "Could not load students.", "error");
      return;
    }
    state.students = (payload.data || []).map(toStudent).filter(Boolean);
    renderApp();
  } catch (error) {
    showToast(error.message, "error");
  }
}

// ===== ADDED: Teacher Management Feature - START =====
async function loadTeachers({ silent = false } = {}) {
  try {
    const payload = await api.command("Display All Teachers");
    if (!payload.success) {
      if (!silent) showToast(payload.message || "Could not load teachers.", "error");
      return;
    }
    state.teachers = (payload.data || []).map(toTeacher).filter(Boolean);
    renderApp();
  } catch (error) {
    showToast(error.message, "error");
  }
}
// ===== ADDED: Teacher Management Feature - END =====

// ===== ADDED: Course Management Feature - START =====
async function loadCourses({ silent = false } = {}) {
  try {
    const payload = await api.command("Display All Courses");
    if (!payload.success) {
      if (!silent) showToast(payload.message || "Could not load courses.", "error");
      return;
    }
    state.courses = (payload.data || []).map(toCourse).filter(Boolean);
    if (
      state.enrollmentCourseFilter !== "all" &&
      !state.courses.some(
        (course) => String(course.course_id) === String(state.enrollmentCourseFilter)
      )
    ) {
      state.enrollmentCourseFilter = "all";
    }
    renderApp();
  } catch (error) {
    showToast(error.message, "error");
  }
}
// ===== ADDED: Course Management Feature - END =====

async function loadEnrollments({ silent = false } = {}) {
  try {
    const payload = await api.command("Display All Enrollments");
    if (!payload.success) {
      if (!silent) showToast(payload.message || "Could not load course enrollments.", "error");
      return;
    }
    state.enrollments = (payload.data || []).map(toEnrollment).filter(Boolean);
    renderApp();
  } catch (error) {
    if (!silent) showToast(error.message, "error");
  }
}

// ===== ADDED: Teacher Allocated Students Feature - START =====
async function loadAllocations({ silent = false } = {}) {
  try {
    const payload = await api.command("Display All Allocations");
    if (!payload.success) {
      if (!silent) showToast(payload.message || "Could not load allocations.", "error");
      return;
    }
    state.allocations = (payload.data || []).map(toAllocation).filter(Boolean);
    renderApp();
  } catch (error) {
    showToast(error.message, "error");
  }
}

async function loadMyAllocations({ silent = false } = {}) {
  try {
    const payload = await api.command("View_My_Allocated_Students");
    if (!payload.success) {
      state.allocations = [];
      if (!silent) showToast(payload.message || "Could not load your students.", "error");
      renderApp();
      return;
    }
    state.allocations = (payload.data || []).map(toAllocation).filter(Boolean);
    renderApp();
  } catch (error) {
    showToast(error.message, "error");
  }
}
// ===== ADDED: Teacher Allocated Students Feature - END =====

async function loadCourseToppers({ silent = false } = {}) {
  if (state.courseToppersLoading) return;
  state.courseToppersLoading = true;
  renderApp();
  try {
    const payload = await api.command("course_toppers");
    state.courseToppersLoaded = true;
    if (!payload.success) {
      state.courseToppers = [];
      if (!silent) showToast(payload.message || "Course toppers are not available yet.", "warning");
      return;
    }
    state.courseToppers = payload.data || [];
  } catch (error) {
    if (!silent) showToast(error.message, "error");
  } finally {
    state.courseToppersLoading = false;
    renderApp();
  }
}

async function loadResultsAndStats({ silent = false } = {}) {
  try {
    const [resultsPayload, statsPayload] = await Promise.all([
      api.command("Display All Result"),
      api.command("result_statistics"),
    ]);

    if (resultsPayload.success) {
      state.results = (resultsPayload.data || []).map(toResult).filter(Boolean);
    } else if (!silent) {
      showToast(resultsPayload.message || "Could not load marks records.", "error");
    }

    if (statsPayload.success) {
      state.stats = statsPayload.data;
    } else if (!silent) {
      showToast(statsPayload.message || "Could not load statistics.", "warning");
    }

    renderApp();
  } catch (error) {
    if (!silent) showToast(error.message, "error");
  }
}

async function loadProfile({ silent = false } = {}) {
  const referenceId = Number(state.user?.reference_id);
  if (!referenceId) {
    state.profile = null;
    if (!silent) {
      showToast("This account is not linked to a student record.", "warning");
    }
    return;
  }

  try {
    const payload = await api.command("Search_Student", { id: referenceId });
    if (!payload.success) {
      state.profile = null;
      if (!silent) showToast(payload.message || "Could not load profile.", "error");
      renderApp();
      return;
    }
    state.profile = toStudent(payload.data);
    renderApp();
  } catch (error) {
    showToast(error.message, "error");
  }
}

async function handleSearch(form) {
  const id = Number(field(form, "id").value);
  if (!Number.isFinite(id) || id < 1) {
    showToast("Enter a valid student ID.", "warning");
    return;
  }

  setFormBusy(form, true);
  try {
    const payload = await api.command("Search_Student", { id });
    if (!payload.success) {
      state.searchResult = null;
      renderApp();
      showToast(payload.message || "Student not found.", "error");
      return;
    }
    state.searchResult = toStudent(payload.data);
    renderApp();
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    setFormBusy(form, false);
  }
}

// ===== ADDED: Teacher Management Feature - START =====
async function handleTeacherSearch(form) {
  const t_id = Number(field(form, "t_id").value);
  if (!Number.isFinite(t_id) || t_id < 1) {
    showToast("Enter a valid teacher ID.", "warning");
    return;
  }

  setFormBusy(form, true);
  try {
    const payload = await api.command("Search_Teacher", { t_id });
    if (!payload.success) {
      state.teacherSearch = null;
      renderApp();
      showToast(payload.message || "Teacher not found.", "error");
      return;
    }
    state.teacherSearch = toTeacher(payload.data);
    renderApp();
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    setFormBusy(form, false);
  }
}
// ===== ADDED: Teacher Management Feature - END =====

// ===== ADDED: Course Management Feature - START =====
async function handleCourseSearch(form) {
  const co_id = Number(field(form, "co_id").value);
  if (!Number.isFinite(co_id) || co_id < 1) {
    showToast("Enter a valid course ID.", "warning");
    return;
  }

  setFormBusy(form, true);
  try {
    const payload = await api.command("Search_Course", { co_id });
    if (!payload.success) {
      state.courseSearch = null;
      renderApp();
      showToast(payload.message || "Course not found.", "error");
      return;
    }
    state.courseSearch = toCourse(payload.data);
    renderApp();
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    setFormBusy(form, false);
  }
}
// ===== ADDED: Course Management Feature - END =====

// ===== ADDED: Teacher Allocated Students Feature - START =====
async function handleAllocate(form) {
  const payload = {
    teacher_id: Number(field(form, "teacher_id").value),
    student_id: Number(field(form, "student_id").value),
    course_id: Number(field(form, "course_id").value),
  };

  if (
    !Number.isFinite(payload.teacher_id) ||
    payload.teacher_id < 1 ||
    !Number.isFinite(payload.student_id) ||
    payload.student_id < 1 ||
    !Number.isFinite(payload.course_id) ||
    payload.course_id < 1
  ) {
    showToast("Fill in valid teacher, student and course IDs.", "warning");
    return;
  }

  setFormBusy(form, true);
  try {
    const response = await api.command("Allocate_Student", payload);
    if (!response.success) {
      showToast(response.message || "Could not allocate student.", "error");
      return;
    }
    form.reset();
    showToast(response.message || "Student allocated.", "success");
    await loadAllocations({ silent: true });
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    setFormBusy(form, false);
  }
}
// ===== ADDED: Teacher Allocated Students Feature - END =====

// ===== ADDED: Student Login Management Feature - START =====
async function handleSetCredentials(form) {
  const payload = {
    id: Number(field(form, "id").value),
    user_name: String(field(form, "user_name").value || "").trim(),
    password: String(field(form, "password").value || ""),
  };

  if (!Number.isFinite(payload.id) || payload.id < 1 || !payload.user_name) {
    showToast("Enter a valid student ID and username.", "warning");
    return;
  }
  if (payload.password.length < 8) {
    showToast("Password must contain at least 8 characters.", "warning");
    return;
  }

  setFormBusy(form, true);
  try {
    const response = await api.command("Set_Student_Credentials", payload);
    if (!response.success) {
      showToast(response.message || "Could not save credentials.", "error");
      return;
    }
    form.reset();
    showToast(response.message || "Student credentials saved.", "success");
    await loadStudents({ silent: true });
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    setFormBusy(form, false);
  }
}
// ===== ADDED: Student Login Management Feature - END =====

async function handleAddMarks(form) {
  const payload = {
    id: Number(field(form, "id").value),
    co_id: Number(field(form, "co_id").value),
    t_id: Number(field(form, "t_id").value),
    marks: Number(field(form, "marks").value),
  };

  if (
    !Number.isFinite(payload.id) ||
    !Number.isFinite(payload.co_id) ||
    !Number.isFinite(payload.t_id) ||
    !Number.isFinite(payload.marks) ||
    payload.marks < 0 ||
    payload.marks > 100
  ) {
    showToast("Fill in valid IDs and marks between 0 and 100.", "warning");
    return;
  }

  setFormBusy(form, true);
  try {
    const response = await api.command("Add_Marks", payload);
    if (!response.success) {
      showToast(response.message || "Could not save marks.", "error");
      return;
    }
    showToast(response.message || "Marks saved successfully.", "success");
    renderApp();
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    setFormBusy(form, false);
  }
}

async function handleCalculate(form) {
  const id = Number(field(form, "id").value);
  if (!Number.isFinite(id) || id < 1) {
    showToast("Enter a valid student ID.", "warning");
    return;
  }

  setFormBusy(form, true);
  try {
    const payload = await api.command("calculate_result", { id });
    if (!payload.success) {
      state.result = null;
      state.calcId = String(id);
      renderApp();
      showToast(payload.message || "No marks found for this student.", "warning");
      return;
    }
    state.calcId = String(id);
    state.result = {
      studentId: id,
      total: payload.total,
      percentage: payload.percentage,
      status: payload.status,
    };
    renderApp();
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    setFormBusy(form, false);
  }
}

async function deleteStudent(id) {
  const student = state.students.find((item) => String(item.id) === String(id));
  const label = student ? `student #${id} (${student.name})` : `student #${id}`;
  if (
    !window.confirm(
      `Delete ${label} and remove their course enrollments, teacher allocations, marks, and student login? This action cannot be undone.`
    )
  ) {
    return;
  }

  try {
    const payload = await api.command("Delete_Student", { id: Number(id) });
    if (!payload.success) {
      showToast(payload.message || "Could not delete student.", "error");
      return;
    }
    state.searchResult = null;
    showToast("Student deleted.", "success");
    await loadStudents({ silent: true });
  } catch (error) {
    showToast(error.message, "error");
  }
}

async function deleteResult(roll) {
  if (
    !window.confirm(
      `Delete marks record #${roll}? This action cannot be undone.`
    )
  ) {
    return;
  }

  try {
    const payload = await api.command("Delete_Marks", { roll: Number(roll) });
    if (!payload.success) {
      showToast(payload.message || "Could not delete marks record.", "error");
      return;
    }
    showToast("Marks record deleted.", "success");
    await loadResultsAndStats({ silent: true });
  } catch (error) {
    showToast(error.message, "error");
  }
}

// ===== ADDED: Teacher Management Feature - START =====
async function deleteTeacher(id) {
  const teacher = state.teachers.find(
    (item) => String(item.teacher_id) === String(id)
  );
  const label = teacher
    ? `teacher #${id} (${teacher.teacher_name})`
    : `teacher #${id}`;
  if (!window.confirm(`Delete ${label}? This action cannot be undone.`)) return;

  try {
    const payload = await api.command("Delete_Teacher", { t_id: Number(id) });
    if (!payload.success) {
      showToast(payload.message || "Could not delete teacher.", "error");
      return;
    }
    state.teacherSearch = null;
    showToast("Teacher deleted.", "success");
    await loadTeachers({ silent: true });
  } catch (error) {
    showToast(error.message, "error");
  }
}
// ===== ADDED: Teacher Management Feature - END =====

// ===== ADDED: Course Management Feature - START =====
async function deleteCourse(id) {
  const course = state.courses.find(
    (item) => String(item.course_id) === String(id)
  );
  const label = course
    ? `course #${id} (${course.course_name})`
    : `course #${id}`;
  if (!window.confirm(`Delete ${label}? This action cannot be undone.`)) return;

  try {
    const payload = await api.command("Delete_Course", { co_id: Number(id) });
    if (!payload.success) {
      showToast(payload.message || "Could not delete course.", "error");
      return;
    }
    state.courseSearch = null;
    showToast("Course deleted.", "success");
    await loadCourses({ silent: true });
  } catch (error) {
    showToast(error.message, "error");
  }
}
// ===== ADDED: Course Management Feature - END =====

// ===== ADDED: Teacher Allocated Students Feature - START =====
async function removeAllocation(teacherId, studentId, courseId) {
  if (
    !window.confirm(
      `Remove allocation of student #${studentId} from teacher #${teacherId} for course #${courseId}?`
    )
  ) {
    return;
  }

  try {
    const payload = await api.command("Remove_Allocation", {
      teacher_id: Number(teacherId),
      student_id: Number(studentId),
      course_id: Number(courseId),
    });
    if (!payload.success) {
      showToast(payload.message || "Could not remove allocation.", "error");
      return;
    }
    showToast("Allocation removed.", "success");
    await loadAllocations({ silent: true });
  } catch (error) {
    showToast(error.message, "error");
  }
}
// ===== ADDED: Teacher Allocated Students Feature - END =====

async function handleEnrollStudent(form) {
  const studentId = Number(field(form, "student_id").value);
  const courseId = Number(field(form, "course_id").value);
  if (!Number.isInteger(studentId) || studentId < 1 || !Number.isInteger(courseId) || courseId < 1) {
    showToast("Select a valid student and course.", "warning");
    return;
  }

  setFormBusy(form, true);
  try {
    const payload = await api.command("Enroll_Student", {
      student_id: studentId,
      course_id: courseId,
    });
    if (!payload.success) {
      showToast(payload.message || "Could not enroll student.", "error");
      return;
    }
    showToast(payload.message || "Student enrolled successfully.", "success");
    form.reset();
    await loadEnrollments({ silent: true });
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    setFormBusy(form, false);
  }
}

async function removeEnrollment(studentId, courseId) {
  const student = state.students.find((item) => String(item.id) === String(studentId));
  const course = state.courses.find((item) => String(item.course_id) === String(courseId));
  const studentLabel = student ? `${student.name} (#${studentId})` : `student #${studentId}`;
  const courseLabel = course ? `${course.course_name} (#${courseId})` : `course #${courseId}`;
  if (!window.confirm(`Remove ${studentLabel} from ${courseLabel}?`)) return;

  try {
    const payload = await api.command("Remove_Enrollment", {
      student_id: Number(studentId),
      course_id: Number(courseId),
    });
    if (!payload.success) {
      showToast(payload.message || "Could not remove course enrollment.", "error");
      return;
    }
    showToast("Course enrollment removed.", "success");
    await loadEnrollments({ silent: true });
  } catch (error) {
    showToast(error.message, "error");
  }
}

function openResultModal(record) {
  if (modalOpen || !record) return;
  modalOpen = true;

  const isTeacher = state.user.role === "teacher";
  const teacherId = isTeacher
    ? state.user.reference_id ?? ""
    : record.teacher_id;
  const overlay = document.createElement("div");
  overlay.className = "modal-overlay";
  overlay.innerHTML = `
    <div class="modal" role="dialog" aria-modal="true" aria-labelledby="result-modal-title">
      <div class="modal-head">
        <div>
          <h3 id="result-modal-title">Edit marks</h3>
          <p>Update the details for marks record #${esc(record.roll)}.</p>
        </div>
        <button class="icon-btn" type="button" data-modal-close title="Close">${icon("close")}</button>
      </div>
      <form class="modal-form">
        <div class="form-grid">
          <div class="field">
            <label>Roll</label>
            <input name="roll" type="number" value="${esc(record.roll)}" readonly>
          </div>
          <div class="field">
            <label>Student ID</label>
            <input name="id" type="number" min="1" required value="${esc(record.student_id)}">
          </div>
          <div class="field">
            <label>Course ID</label>
            <input name="co_id" type="number" min="1" required value="${esc(record.course_id)}">
          </div>
          <div class="field">
            <label>Teacher ID</label>
            <input name="t_id" type="number" min="1" required value="${esc(teacherId)}" ${isTeacher ? "readonly" : ""}>
          </div>
          <div class="field">
            <label>Marks (0 - 100)</label>
            <input name="marks" type="number" min="0" max="100" step="0.01" required value="${esc(record.marks)}">
          </div>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn ghost" data-modal-close>Cancel</button>
          <button type="submit" class="btn primary">${icon("check")} Save changes</button>
        </div>
      </form>
    </div>`;

  document.body.appendChild(overlay);
  document.body.classList.add("modal-open");
  requestAnimationFrame(() => overlay.classList.add("show"));

  const close = () => {
    if (!modalOpen) return;
    modalOpen = false;
    overlay.classList.remove("show");
    document.body.classList.remove("modal-open");
    window.setTimeout(() => overlay.remove(), 160);
  };

  overlay.addEventListener("click", (event) => {
    if (event.target === overlay || event.target.closest("[data-modal-close]")) {
      close();
    }
  });

  overlay.querySelector("form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const payload = {
      roll: Number(field(form, "roll").value),
      id: Number(field(form, "id").value),
      co_id: Number(field(form, "co_id").value),
      t_id: Number(field(form, "t_id").value),
      marks: Number(field(form, "marks").value),
    };

    if (
      !Number.isFinite(payload.roll) ||
      !Number.isFinite(payload.id) ||
      !Number.isFinite(payload.co_id) ||
      !Number.isFinite(payload.t_id) ||
      !Number.isFinite(payload.marks) ||
      payload.marks < 0 ||
      payload.marks > 100
    ) {
      showToast("Fill in valid IDs and marks between 0 and 100.", "warning");
      return;
    }

    setFormBusy(form, true);
    try {
      const response = await api.command("Update_Marks", payload);
      if (!response.success) {
        showToast(response.message || "Could not update marks.", "error");
        return;
      }
      showToast(response.message || "Marks updated.", "success");
      close();
      await loadResultsAndStats({ silent: true });
    } catch (error) {
      showToast(error.message, "error");
    } finally {
      setFormBusy(form, false);
    }
  });
}

function openStudentModal(student) {
  if (modalOpen) return;
  modalOpen = true;

  const editing = Boolean(student);
  const overlay = document.createElement("div");
  overlay.className = "modal-overlay";
  overlay.innerHTML = `
    <div class="modal" role="dialog" aria-modal="true" aria-labelledby="student-modal-title">
      <div class="modal-head">
        <div>
          <h3 id="student-modal-title">${editing ? "Edit student" : "Add student"}</h3>
          <p>${editing ? "Update the student's details." : "Create a new record in the database."}</p>
        </div>
        <button class="icon-btn" type="button" data-modal-close title="Close">${icon("close")}</button>
      </div>
      <form class="modal-form">
        <div class="form-grid">
          <div class="field">
            <label>Student ID</label>
            <input name="id" type="number" min="1" required value="${editing ? esc(student.id) : ""}" ${editing ? "readonly" : ""} placeholder="e.g. 101">
          </div>
          <div class="field">
            <label>Age</label>
            <input name="age" type="number" min="1" required value="${editing ? esc(student.age) : ""}" placeholder="e.g. 20">
          </div>
        </div>
        <div class="field">
          <label>Full name</label>
          <input name="name" required maxlength="20" value="${editing ? esc(student.name) : ""}" placeholder="e.g. Rahul Sharma">
        </div>
        <div class="modal-actions">
          <button type="button" class="btn ghost" data-modal-close>Cancel</button>
          <button type="submit" class="btn primary">${editing ? icon("check") + " Save changes" : icon("plus") + " Add student"}</button>
        </div>
      </form>
    </div>`;

  document.body.appendChild(overlay);
  document.body.classList.add("modal-open");
  requestAnimationFrame(() => overlay.classList.add("show"));

  const close = () => {
    if (!modalOpen) return;
    modalOpen = false;
    overlay.classList.remove("show");
    document.body.classList.remove("modal-open");
    window.setTimeout(() => overlay.remove(), 160);
  };

  overlay.addEventListener("click", (event) => {
    if (event.target === overlay || event.target.closest("[data-modal-close]")) {
      close();
    }
  });

  overlay.querySelector("form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const payload = {
      id: Number(field(form, "id").value),
      name: String(field(form, "name").value || "").trim(),
      age: Number(field(form, "age").value),
    };

    if (!Number.isFinite(payload.id) || payload.id < 1 || !payload.name || !Number.isFinite(payload.age) || payload.age < 1) {
      showToast("Fill in a valid ID, name and age.", "warning");
      return;
    }

    setFormBusy(form, true);
    try {
      const request = editing ? "update_student" : "Add_Student";
      const response = await api.command(request, payload);
      if (!response.success) {
        showToast(response.message || "Could not save student.", "error");
        return;
      }
      showToast(response.message || "Student saved.", "success");
      close();
      state.searchResult = null;
      await loadStudents({ silent: true });
    } catch (error) {
      showToast(error.message, "error");
    } finally {
      setFormBusy(form, false);
    }
  });
}

// ===== ADDED: Teacher Management Feature - START =====
function openTeacherModal(teacher) {
  if (modalOpen) return;
  modalOpen = true;

  const editing = Boolean(teacher);
  const joining =
    teacher && teacher.joining_date
      ? String(teacher.joining_date).slice(0, 10)
      : "";
  const overlay = document.createElement("div");
  overlay.className = "modal-overlay";
  overlay.innerHTML = `
    <div class="modal" role="dialog" aria-modal="true" aria-labelledby="teacher-modal-title">
      <div class="modal-head">
        <div>
          <h3 id="teacher-modal-title">${editing ? "Edit teacher" : "Add teacher"}</h3>
          <p>${editing ? "Update the teacher's details." : "Create a new teacher record in the database."}</p>
        </div>
        <button class="icon-btn" type="button" data-modal-close title="Close">${icon("close")}</button>
      </div>
      <form class="modal-form">
        <div class="form-grid">
          <div class="field">
            <label>Teacher ID</label>
            <input name="t_id" type="number" min="1" required value="${editing ? esc(teacher.teacher_id) : ""}" ${editing ? "readonly" : ""} placeholder="e.g. 301">
          </div>
          <div class="field">
            <label>Salary</label>
            <input name="salary" type="number" min="0" step="0.01" required value="${editing ? esc(teacher.salary) : ""}" placeholder="e.g. 45000">
          </div>
        </div>
        <div class="field">
          <label>Full name</label>
          <input name="t_name" required maxlength="20" value="${editing ? esc(teacher.teacher_name) : ""}" placeholder="e.g. Amit Verma">
        </div>
        <div class="field">
          <label>Joining date</label>
          <input name="j_o_d" type="date" required value="${esc(joining)}">
        </div>
        <div class="modal-actions">
          <button type="button" class="btn ghost" data-modal-close>Cancel</button>
          <button type="submit" class="btn primary">${editing ? icon("check") + " Save changes" : icon("plus") + " Add teacher"}</button>
        </div>
      </form>
    </div>`;

  document.body.appendChild(overlay);
  document.body.classList.add("modal-open");
  requestAnimationFrame(() => overlay.classList.add("show"));

  const close = () => {
    if (!modalOpen) return;
    modalOpen = false;
    overlay.classList.remove("show");
    document.body.classList.remove("modal-open");
    window.setTimeout(() => overlay.remove(), 160);
  };

  overlay.addEventListener("click", (event) => {
    if (event.target === overlay || event.target.closest("[data-modal-close]")) {
      close();
    }
  });

  overlay.querySelector("form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const payload = {
      t_id: Number(field(form, "t_id").value),
      t_name: String(field(form, "t_name").value || "").trim(),
      j_o_d: String(field(form, "j_o_d").value || ""),
      salary: Number(field(form, "salary").value),
    };

    if (
      !Number.isFinite(payload.t_id) ||
      payload.t_id < 1 ||
      !payload.t_name ||
      !/^\d{4}-\d{2}-\d{2}$/.test(payload.j_o_d) ||
      !Number.isFinite(payload.salary) ||
      payload.salary < 0
    ) {
      showToast("Fill in a valid ID, name, joining date and salary.", "warning");
      return;
    }

    setFormBusy(form, true);
    try {
      const request = editing ? "Update_Teacher" : "Add_Teacher";
      const response = await api.command(request, payload);
      if (!response.success) {
        showToast(response.message || "Could not save teacher.", "error");
        return;
      }
      showToast(response.message || "Teacher saved.", "success");
      close();
      state.teacherSearch = null;
      await loadTeachers({ silent: true });
    } catch (error) {
      showToast(error.message, "error");
    } finally {
      setFormBusy(form, false);
    }
  });
}
// ===== ADDED: Teacher Management Feature - END =====

// ===== ADDED: Course Management Feature - START =====
function openCourseModal(course) {
  if (modalOpen) return;
  modalOpen = true;

  const editing = Boolean(course);
  const overlay = document.createElement("div");
  overlay.className = "modal-overlay";
  overlay.innerHTML = `
    <div class="modal" role="dialog" aria-modal="true" aria-labelledby="course-modal-title">
      <div class="modal-head">
        <div>
          <h3 id="course-modal-title">${editing ? "Edit course" : "Add course"}</h3>
          <p>${editing ? "Update the course's details." : "Create a new course record in the database."}</p>
        </div>
        <button class="icon-btn" type="button" data-modal-close title="Close">${icon("close")}</button>
      </div>
      <form class="modal-form">
        <div class="form-grid">
          <div class="field">
            <label>Course ID</label>
            <input name="co_id" type="number" min="1" required value="${editing ? esc(course.course_id) : ""}" ${editing ? "readonly" : ""} placeholder="e.g. 201">
          </div>
          <div class="field">
            <label>Fees</label>
            <input name="fees" type="number" min="0" step="0.01" required value="${editing ? esc(course.course_fees) : ""}" placeholder="e.g. 12000">
          </div>
        </div>
        <div class="field">
          <label>Course name</label>
          <input name="co_name" required maxlength="20" value="${editing ? esc(course.course_name) : ""}" placeholder="e.g. Data Structures">
        </div>
        <div class="modal-actions">
          <button type="button" class="btn ghost" data-modal-close>Cancel</button>
          <button type="submit" class="btn primary">${editing ? icon("check") + " Save changes" : icon("plus") + " Add course"}</button>
        </div>
      </form>
    </div>`;

  document.body.appendChild(overlay);
  document.body.classList.add("modal-open");
  requestAnimationFrame(() => overlay.classList.add("show"));

  const close = () => {
    if (!modalOpen) return;
    modalOpen = false;
    overlay.classList.remove("show");
    document.body.classList.remove("modal-open");
    window.setTimeout(() => overlay.remove(), 160);
  };

  overlay.addEventListener("click", (event) => {
    if (event.target === overlay || event.target.closest("[data-modal-close]")) {
      close();
    }
  });

  overlay.querySelector("form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const payload = {
      co_id: Number(field(form, "co_id").value),
      co_name: String(field(form, "co_name").value || "").trim(),
      fees: Number(field(form, "fees").value),
    };

    if (
      !Number.isFinite(payload.co_id) ||
      payload.co_id < 1 ||
      !payload.co_name ||
      !Number.isFinite(payload.fees) ||
      payload.fees < 0
    ) {
      showToast("Fill in a valid ID, name and fees.", "warning");
      return;
    }

    setFormBusy(form, true);
    try {
      const request = editing ? "Update_Course" : "Add_Course";
      const response = await api.command(request, payload);
      if (!response.success) {
        showToast(response.message || "Could not save course.", "error");
        return;
      }
      showToast(response.message || "Course saved.", "success");
      close();
      state.courseSearch = null;
      await loadCourses({ silent: true });
    } catch (error) {
      showToast(error.message, "error");
    } finally {
      setFormBusy(form, false);
    }
  });
}
// ===== ADDED: Course Management Feature - END =====

function onAppClick(event) {
  const navTarget = event.target.closest("[data-nav]");
  if (navTarget) {
    event.preventDefault();
    enterView(navTarget.dataset.nav);
    return;
  }

  const actionTarget = event.target.closest("[data-action]");
  if (!actionTarget) return;

  const action = actionTarget.dataset.action;
  switch (action) {
    case "toggle-sidebar":
      state.sidebarOpen = true;
      renderApp();
      break;
    case "close-sidebar":
      state.sidebarOpen = false;
      renderApp();
      break;
    case "logout":
      handleLogout();
      break;
    case "add-student":
      openStudentModal();
      break;
    case "edit-student": {
      const id = actionTarget.dataset.id;
      const student = state.students.find((item) => String(item.id) === String(id));
      if (student) openStudentModal(student);
      break;
    }
    case "delete-student":
      deleteStudent(actionTarget.dataset.id);
      break;
    case "refresh-students":
      loadStudents();
      break;
    case "load-topper":
      loadCourseToppers();
      break;
    case "load-stats":
    case "refresh-results":
      loadResultsAndStats();
      break;
    case "edit-result": {
      const roll = actionTarget.dataset.roll;
      const record = state.results.find(
        (item) => String(item.roll) === String(roll)
      );
      if (record) openResultModal(record);
      break;
    }
    case "delete-result":
      deleteResult(actionTarget.dataset.roll);
      break;
    case "clear-search":
      state.searchResult = null;
      renderApp();
      break;
    case "refresh-profile":
      loadProfile();
      break;
    // ===== ADDED: Teacher Management Feature - actions =====
    case "add-teacher":
      openTeacherModal();
      break;
    case "edit-teacher": {
      const id = actionTarget.dataset.id;
      const teacher = state.teachers.find(
        (item) => String(item.teacher_id) === String(id)
      );
      if (teacher) openTeacherModal(teacher);
      break;
    }
    case "delete-teacher":
      deleteTeacher(actionTarget.dataset.id);
      break;
    case "refresh-teachers":
      loadTeachers();
      break;
    case "clear-teacher-search":
      state.teacherSearch = null;
      renderApp();
      break;
    // ===== ADDED: Course Management Feature - actions =====
    case "add-course":
      openCourseModal();
      break;
    case "edit-course": {
      const id = actionTarget.dataset.id;
      const course = state.courses.find(
        (item) => String(item.course_id) === String(id)
      );
      if (course) openCourseModal(course);
      break;
    }
    case "delete-course":
      deleteCourse(actionTarget.dataset.id);
      break;
    case "refresh-courses":
      loadCourses();
      break;
    case "refresh-enrollments":
      loadEnrollments();
      break;
    case "clear-course-search":
      state.courseSearch = null;
      renderApp();
      break;
    // ===== ADDED: Teacher Allocated Students Feature - actions =====
    case "refresh-allocations":
      loadAllocations();
      break;
    case "refresh-my-allocations":
      loadMyAllocations();
      break;
    case "remove-allocation":
      removeAllocation(
        actionTarget.dataset.teacher,
        actionTarget.dataset.student,
        actionTarget.dataset.course
      );
      break;
    case "remove-enrollment":
      removeEnrollment(actionTarget.dataset.student, actionTarget.dataset.course);
      break;
    default:
      break;
  }
}

function onAppChange(event) {
  if (!event.target.matches("[data-enrollment-course-filter]")) return;
  state.enrollmentCourseFilter = event.target.value || "all";
  renderApp();
}

function onAppSubmit(event) {
  const form = event.target.closest("form[data-form]");
  if (!form) return;
  event.preventDefault();

  switch (form.dataset.form) {
    case "login":
      handleLogin(form);
      break;
    case "search-student":
      handleSearch(form);
      break;
    case "add-marks":
      handleAddMarks(form);
      break;
    case "calculate-result":
      handleCalculate(form);
      break;
    // ===== ADDED: Teacher, Course, Allocation and Login forms =====
    case "search-teacher":
      handleTeacherSearch(form);
      break;
    case "search-course":
      handleCourseSearch(form);
      break;
    case "allocate-student":
      handleAllocate(form);
      break;
    case "enroll-student":
      handleEnrollStudent(form);
      break;
    case "set-credentials":
      handleSetCredentials(form);
      break;
    default:
      break;
  }
}

function boot() {
  app.addEventListener("click", onAppClick);
  app.addEventListener("change", onAppChange);
  app.addEventListener("submit", onAppSubmit);

  window.addEventListener("nsms:session-expired", () => {
    state.user = null;
    state.view = "";
    state.profile = null;
    state.result = null;
    state.searchResult = null;
    // ===== ADDED: Reset teacher, course and allocation state on session expiry =====
    state.teachers = [];
    state.courses = [];
    state.allocations = [];
    state.enrollments = [];
    state.enrollmentCourseFilter = "all";
    state.teacherSearch = null;
    state.courseSearch = null;
    state.results = [];
    state.stats = null;
    state.courseToppers = [];
    state.courseToppersLoaded = false;
    state.courseToppersLoading = false;
    renderLogin();
    showToast("Your session expired. Please sign in again.", "warning");
  });

  if (api.getToken() && state.user) {
    state.view = firstView();
    renderApp();
    syncHealth();
    if (state.user.role === "admin") {
      loadStudents({ silent: true });
    }
    loadCourseToppers({ silent: true });
    if (state.user.role === "student") loadProfile({ silent: true });
  } else {
    renderLogin();
    syncHealth();
  }
}

boot();
