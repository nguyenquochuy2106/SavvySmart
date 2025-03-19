document.addEventListener("DOMContentLoaded", async function () {
    const response = await fetch("http://localhost:8000/stats");
    const stats = await response.json();

    new Chart(document.getElementById("spendingChart"), {
        type: "doughnut",
        data: {
            labels: stats.categories,
            datasets: [{
                data: stats.amounts,
                backgroundColor: ["#4f46e5", "#3b82f6", "#22c55e", "#ef4444"],
            }]
        }
    });
});
