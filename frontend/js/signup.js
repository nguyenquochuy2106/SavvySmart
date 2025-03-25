
document.getElementById("openCamera").addEventListener("click", function() {
    let video = document.getElementById("video");
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(err => console.log("Error: " + err));
});

document.getElementById("capture").addEventListener("click", function() {
    let video = document.getElementById("video");
    let canvas = document.getElementById("canvas");
    let context = canvas.getContext("2d");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
});

document.getElementById("signup").addEventListener("click", async function() {
    let name = document.getElementById("name").value;
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let repassword = document.getElementById("repassword").value;
    let canvas = document.getElementById("canvas");
    let image = canvas.toDataURL("image/png").split(",")[1];
    
    if (password !== repassword) {
        alert("Passwords do not match");
        return;
    }

    let response = await fetch("http://localhost:8000/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password, image })
    });
    let result = await response.json();
    alert(result.message);
});
