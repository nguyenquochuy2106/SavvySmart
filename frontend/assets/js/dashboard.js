document.addEventListener("DOMContentLoaded", async function () {
    const response = await fetch("http://localhost:8000/user/me");
    const user = await response.json();

    document.getElementById("user-name").textContent = user.full_name;
    document.getElementById("balance").textContent = user.balance.toFixed(2);
});
