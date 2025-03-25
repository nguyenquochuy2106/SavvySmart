const API_URL = "http://127.0.0.1:8000";  

async function signup() {
    const username = document.getElementById("signup-username").value;
    const email = document.getElementById("signup-email").value;
    const password = document.getElementById("signup-password").value;
    const confirmPassword = document.getElementById("signup-confirm-password").value;
    
    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    const imageBase64 = await captureImageBase64();  

    const response = await fetch(`${API_URL}/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password, image: imageBase64 })
    });

    const result = await response.json();
    if (response.ok) {
        alert("Sign up successful!");
        window.location.href = "login.html";
    } else {
        alert(result.detail || "Sign up failed!");
    }
}

async function faceIdLogin() {
    const imageBase64 = await captureImageBase64();  

    const response = await fetch(`${API_URL}/face-login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: imageBase64 })
    });

    const result = await response.json();
    if (response.ok) {
        alert("FaceID Login successful!");
        window.location.href = "dashboard.html";
    } else {
        alert(result.detail || "FaceID Login failed!");
    }
}

async function captureImageBase64() {
    const video = document.createElement("video");
    video.style.display = "none";
    document.body.appendChild(video);

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        await video.play();

        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext("2d");
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        const imageBase64 = canvas.toDataURL("image/jpeg");
        stream.getTracks().forEach(track => track.stop());
        document.body.removeChild(video);

        return imageBase64;
    } catch (error) {
        console.error("Error capturing image:", error);
        alert("Failed to capture image!");
        return null;
    }
}
