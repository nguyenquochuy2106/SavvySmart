document.addEventListener("DOMContentLoaded", function () {
    // Start camera for FaceID
    const video = document.getElementById("video");
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => video.srcObject = stream)
        .catch(err => console.error("Camera access denied:", err));
});

function captureFace() {
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const context = canvas.getContext("2d");

    // Capture frame from video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert to Base64
    const imageBase64 = canvas.toDataURL("image/jpeg").split(',')[1];

    console.log("Captured FaceID Image ✅");

    return imageBase64;  // Return Base64 image
}

// Handle form submission
document.getElementById("register-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const userData = {
        email: document.getElementById("email").value,
        full_name: document.getElementById("full_name").value,
        image: captureFace()
    };

    const response = await fetch("http://localhost:8000/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData)
    });

    const result = await response.json();
    alert(result.message);
});
