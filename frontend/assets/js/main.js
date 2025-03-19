document.addEventListener("DOMContentLoaded", function () {
    console.log("Frontend Loaded ✅");
    
    // Highlight active navbar link
    const path = window.location.pathname;
    document.querySelectorAll(".nav-link").forEach(link => {
        if (link.getAttribute("href") === path) {
            link.classList.add("active");
        }
    });
});
