const API_BASE_URL = "http://localhost:8000";

async function registerUser(username, email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password })
        });

        // Kiểm tra phản hồi từ API
        const data = await response.json();

        if (!response.ok) {
            console.error("API Error:", data);
            throw new Error(data.detail || "Registration failed");
        }
        console.log("User registered successfully:", data);
        alert("Registration successful!");
        // ✅ Điều hướng sang trang login sau khi đăng ký thành công
        window.location.href = "/login";
    } catch (error) {
        console.error("Fetch error:", error);
        alert(`Error: ${error.message}`);
    }
}


async function loginUser(username, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        // Kiểm tra phản hồi từ API
        const data = await response.json();

        if(!response.ok) {
            console.error("API Error:", data);
            throw new Error(data.detail || "Login failed");
        }
        console.log("User logged in successfully:", data);
        alert("Login successful!");
    } catch (error) {
        console.error("Fetch error:", error);
        alert(`Error: ${error.message}`);
    }
} 




// ✅ Gọi hàm này khi submit form
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

// ✅ Gọi hàm này khi login form
document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("login-form");

    if (registerForm) {
        registerForm.addEventListener("submit", async function (event) {
            event.preventDefault();
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            await loginUser(username, password);
        });
    }
});