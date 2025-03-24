class APIService {
    static BASE_URL = "http://localhost:8000";

    static async request(endpoint, method = "GET", data = null) {
        const options = {
            method,
            headers: { "Content-Type": "application/json" }
        };
        if (data) options.body = JSON.stringify(data);
        
        const response = await fetch(`${this.BASE_URL}${endpoint}`, options);
        return response.json();
    }
}

class AuthService {
    static async login(imageBase64) {
        return await APIService.request("/login", "POST", { image: imageBase64 });
    }
    static async register(email, password, full_name, imageBase64) {
        return await APIService.request("/register", "POST", { email, password, full_name, image: imageBase64 });
    }
}

class TransactionService {
    static async getTransactions(userId) {
        return await APIService.request(`/transactions/list?user_id=${userId}`);
    }
    static async addTransaction(userId, amount, category, description) {
        return await APIService.request("/transactions/add", "POST", { user_id: userId, amount, category, description });
    }
}

class BudgetService {
    static async getBudget(userId) {
        return await APIService.request(`/budget?user_id=${userId}`);
    }
    static async updateBudget(userId, budgetData) {
        return await APIService.request("/budget/update", "PUT", { user_id: userId, ...budgetData });
    }
}

class AnalyticsService {
    static async getAnalytics(userId) {
        return await APIService.request(`/analytics?user_id=${userId}`);
    }
}

// 📌 Khởi chạy ứng dụng
document.addEventListener("DOMContentLoaded", async () => {
    const userId = localStorage.getItem("user_id");
    if (!userId) return;

    const transactions = await TransactionService.getTransactions(userId);
    console.log("Transactions:", transactions);

    const budget = await BudgetService.getBudget(userId);
    console.log("Budget:", budget);

    const analytics = await AnalyticsService.getAnalytics(userId);
    console.log("Analytics:", analytics);
});
