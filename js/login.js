async function login() {
  const res = await fetch("http://localhost:5000/api/auth/login", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      email: document.getElementById("email").value,
      password: document.getElementById("password").value
    })
  });

  const data = await res.json();

  if (data.success) {
    window.location.href = "dashboard.html";
  } else {
    alert("Login Failed");
  }
}
