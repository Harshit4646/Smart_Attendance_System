// auth.js
// Handles authentication UI and API interactions for login/logout

/**
 * Listen for login button.
 * On click: collect role, email, password; call POST /auth/login; set session on success.
 * Display error for fail, redirect on success.
 */
document.getElementById('loginBtn')?.addEventListener('click', async function() {
  // TODO: Collect form, call API, handle response
  // Example structure:
  // const role = ...; const email = ...; const pw = ...
  // fetch('/auth/login', ...)
  document.getElementById('loginAlert').style.display = 'block';
  document.getElementById('loginAlert').innerText = 'Login logic not yet implemented.';
});

/**
 * Stub for logout (to be hooked on other dashboards)
 */
function logout() {
  // TODO: Call /auth/logout, clear session, redirect
}
