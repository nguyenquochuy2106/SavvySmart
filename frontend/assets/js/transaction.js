document.addEventListener("DOMContentLoaded", async function () {
    const list = document.getElementById("transaction-list");

    async function loadTransactions() {
        const response = await fetch("http://localhost:8000/transactions");
        const transactions = await response.json();
        list.innerHTML = "";
        transactions.forEach(tx => {
            list.innerHTML += `<li class="list-group-item">${tx.description} - $${tx.amount} <button onclick="deleteTransaction(${tx.id})" class="btn btn-danger btn-sm">X</button></li>`;
        });
    }

    document.getElementById("transaction-form").addEventListener("submit", async function (e) {
        e.preventDefault();
        await fetch("http://localhost:8000/transactions", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                description: document.getElementById("description").value,
                amount: parseFloat(document.getElementById("amount").value)
            })
        });
        loadTransactions();
    });

    window.deleteTransaction = async function (id) {
        await fetch(`http://localhost:8000/transactions/${id}`, { method: "DELETE" });
        loadTransactions();
    };

    loadTransactions();
});
