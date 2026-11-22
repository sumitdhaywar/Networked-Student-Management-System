const TOKEN_KEY = "nsms.token";
const USER_KEY = "nsms.user";

function safeGet(key) {
  try {
    return sessionStorage.getItem(key);
  } catch {
    return null;
  }
}

function safeSet(key, value) {
  try {
    sessionStorage.setItem(key, value);
  } catch {
    /* ignore storage restrictions */
  }
}

function safeRemove(key) {
  try {
    sessionStorage.removeItem(key);
  } catch {
    /* ignore storage restrictions */
  }
}

export function getToken() {
  return safeGet(TOKEN_KEY) || "";
}

export function getUser() {
  const raw = safeGet(USER_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function clearSession() {
  safeRemove(TOKEN_KEY);
  safeRemove(USER_KEY);
}

function saveSession(payload) {
  safeSet(TOKEN_KEY, payload.session_token || "");
  safeSet(
    USER_KEY,
    JSON.stringify({
      user_id: payload.user_id,
      username: payload.username,
      role: payload.role,
      reference_id: payload.reference_id,
    })
  );
}

async function requestJSON(url, options = {}) {
  let response;
  try {
    response = await fetch(url, options);
  } catch {
    throw new Error(
      "Cannot reach the frontend gateway. Make sure gateway.py is running."
    );
  }

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    throw new Error(`The gateway returned an unexpected response (${response.status}).`);
  }

  if (!payload || typeof payload !== "object") {
    throw new Error("The gateway returned an empty response.");
  }

  return payload;
}

export async function login(username, password) {
  const payload = await requestJSON("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (payload.success) {
    saveSession(payload);
  }
  return payload;
}

export async function logout() {
  let payload = { success: true };
  try {
    payload = await requestJSON("/api/logout", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Session-Token": getToken(),
      },
      body: "{}",
    });
  } catch {
    /* clearing the local session still matters */
  }
  clearSession();
  return payload;
}

export async function command(request, data = {}) {
  const payload = await requestJSON("/api/command", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Session-Token": getToken(),
    },
    body: JSON.stringify({ request, data }),
  });

  const message = String(payload.message || "");
  if (
    payload.success === false &&
    /session|authentication required/i.test(message)
  ) {
    clearSession();
    window.dispatchEvent(new CustomEvent("nsms:session-expired"));
  }

  return payload;
}

export async function health() {
  try {
    return await requestJSON("/api/health", { headers: { Accept: "application/json" } });
  } catch {
    return {
      success: false,
      server: { host: "127.0.0.1", port: 5000, reachable: false },
    };
  }
}
