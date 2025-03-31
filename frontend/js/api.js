const API_BASE_URL = "http://localhost:8000";

async function registerUser(username, email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            console.error("API Error:", data);
            throw new Error(data.detail || "Registration failed");
        }
        
        console.log("User registered successfully:", data);
        alert("Registration successful!");
        
        console.log("Before redirect:", window.location);
        
        // ✅ Ensure window.location is not overridden
        if (typeof window.location !== "object") {
            console.warn("window.location was modified! Resetting...");
            window.location = new URL(window.location.href);
        }

        // ✅ Redirect to login page (multiple methods)
        setTimeout(() => {
            try {
                window.location.href = "C:/Users/GIANG_HUY/Desktop/GitHub/SavvySmart/frontend/pages/login.html";
            } catch (e) {
                console.warn("Redirect failed with href. Trying assign.", e);
                window.location.assign("C:/Users/GIANG_HUY/Desktop/GitHub/SavvySmart/frontend/pages/login.html");
            }
        }, 500);
    } catch (error) {
        console.error("Fetch error:", error);
        alert(`Error: ${error.message}`);
    }
}

async function loginUser(emailOrUsername, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email_or_username: emailOrUsername, password }) // ✅ Gửi email hoặc username
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Login failed");
        }

        alert("Login successful!");
        window.location.href = "dashboard.html";  // ✅ Redirect sau khi đăng nhập thành công
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

// ✅ Handle register form submission
document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("register-form");

    if (registerForm) {
        registerForm.addEventListener("submit", async function (event) {
            event.preventDefault();
            const username = document.getElementById("username").value;
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            await registerUser(username, email, password);
        });
    }
});

// ✅ Handle login form submission
document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");

    if (loginForm) {
        loginForm.addEventListener("submit", async function (event) {
            event.preventDefault();
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            await loginUser(username, password);
        });
    }
});
