let transactions = [];
let filteredTransactions = [];

// Categories với màu sắc tương ứng
const categories = {
    salary: { name: 'Salary', color: '#00b894' },
    shopping: { name: 'Shopping', color: '#fd79a8' },
    food: { name: 'Food & Drinks', color: '#ffeaa7' },
    transport: { name: 'Transport', color: '#74b9ff' },
    utilities: { name: 'Utilities', color: '#a29bfe' },
    entertainment: { name: 'Entertainment', color: '#ff7675' },
    others: { name: 'Others', color: '#636e72' }
};

// Khởi tạo trang
function initTransactionsPage() {
    loadMockData();
    initializeDateFilters();
    initializeSearchFilters();
    updateSummaryCards();
    renderTransactions();
    initializeModal();
}

// Load dữ liệu mẫu
function loadMockData() {
    transactions = [
        {
            id: 1,
            date: '2024-03-20',
            type: 'expense',
            category: 'shopping',
            amount: 85.20,
            description: 'Grocery Shopping'
        },
        {
            id: 2,
            date: '2024-03-19',
            type: 'income',
            category: 'salary',
            amount: 3000.00,
            description: 'Monthly Salary'
        }
        // Thêm các giao dịch mẫu khác
    ];
    filteredTransactions = [...transactions];
}

// Khởi tạo bộ lọc ngày tháng
function initializeDateFilters() {
    const presetButtons = document.querySelectorAll('.preset-dates button');
    const customDateInputs = document.querySelector('.custom-date-inputs');

    presetButtons.forEach(button => {
        button.addEventListener('click', () => {
            presetButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            if (button.classList.contains('custom-date')) {
                customDateInputs.style.display = 'flex';
            } else {
                customDateInputs.style.display = 'none';
                const days = parseInt(button.dataset.days);
                setDateRange(days);
            }
        });
    });

    // Set default date range (7 days)
    setDateRange(7);
}

function setDateRange(days) {
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - days);

    document.getElementById('startDate').value = startDate.toISOString().split('T')[0];
    document.getElementById('endDate').value = endDate.toISOString().split('T')[0];

    applyFilters();
}

// Khởi tạo bộ lọc tìm kiếm
function initializeSearchFilters() {
    const searchInput = document.getElementById('searchInput');
    const typeFilter = document.getElementById('typeFilter');
    const categoryFilter = document.getElementById('categoryFilter');

    [searchInput, typeFilter, categoryFilter].forEach(filter => {
        filter.addEventListener('input', applyFilters);
    });
}

// Áp dụng các bộ lọc
function applyFilters() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const type = document.getElementById('typeFilter').value;
    const category = document.getElementById('categoryFilter').value;
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;

    filteredTransactions = transactions.filter(transaction => {
        const matchesSearch = transaction.description.toLowerCase().includes(searchTerm);
        const matchesType = type === 'all' || transaction.type === type;
        const matchesCategory = category === 'all' || transaction.category === category;
        const matchesDate = (!startDate || transaction.date >= startDate) && 
                          (!endDate || transaction.date <= endDate);

        return matchesSearch && matchesType && matchesCategory && matchesDate;
    });

    updateSummaryCards();
    renderTransactions();
}

// Cập nhật thẻ tổng quan
function updateSummaryCards() {
    const totals = filteredTransactions.reduce((acc, trans) => {
        if (trans.type === 'income') {
            acc.income += trans.amount;
        } else {
            acc.expenses += trans.amount;
        }
        return acc;
    }, { income: 0, expenses: 0 });

    const balance = totals.income - totals.expenses;

    document.getElementById('totalIncome').textContent = formatCurrency(totals.income);
    document.getElementById('totalExpenses').textContent = formatCurrency(totals.expenses);
    document.getElementById('netBalance').textContent = formatCurrency(balance);
}

// Hiển thị danh sách giao dịch
function renderTransactions() {
    const tbody = document.getElementById('transactionsBody');
    tbody.innerHTML = filteredTransactions.map(transaction => `
        <tr>
            <td>${formatDate(transaction.date)}</td>
            <td>${transaction.description}</td>
            <td>
                <span class="category-tag" style="background: ${categories[transaction.category].color}20; color: ${categories[transaction.category].color}">
                    ${categories[transaction.category].name}
                </span>
            </td>
            <td class="${transaction.type}">
                ${transaction.type === 'expense' ? '-' : '+'}${formatCurrency(transaction.amount)}
            </td>
            <td>
                <span class="type-tag ${transaction.type}">
                    ${transaction.type.charAt(0).toUpperCase() + transaction.type.slice(1)}
                </span>
            </td>
            <td>
                <button class="btn-icon" onclick="editTransaction(${transaction.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn-icon delete" onclick="deleteTransaction(${transaction.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

// Xử lý modal
function initializeModal() {
    const modal = document.getElementById('transactionModal');
    const closeBtn = modal.querySelector('.close');
    const form = document.getElementById('transactionForm');

    closeBtn.onclick = closeModal;
    window.onclick = (e) => {
        if (e.target === modal) closeModal();
    };

    form.onsubmit = handleTransactionSubmit;
}

function openTransactionModal(transactionId = null) {
    const modal = document.getElementById('transactionModal');
    const form = document.getElementById('transactionForm');
    const modalTitle = modal.querySelector('.modal-header h3');

    if (transactionId) {
        const transaction = transactions.find(t => t.id === transactionId);
        if (transaction) {
            modalTitle.textContent = 'Edit Transaction';
            fillFormWithTransaction(transaction);
            form.dataset.editId = transactionId;
        }
    } else {
        modalTitle.textContent = 'Add New Transaction';
        form.reset();
        delete form.dataset.editId;
    }

    modal.style.display = 'block';
}

function closeModal() {
    document.getElementById('transactionModal').style.display = 'none';
}

function fillFormWithTransaction(transaction) {
    const form = document.getElementById('transactionForm');
    form.querySelector('[name="date"]').value = transaction.date;
    form.querySelector(`[name="type"][value="${transaction.type}"]`).checked = true;
    form.querySelector('[name="category"]').value = transaction.category;
    form.querySelector('[name="amount"]').value = transaction.amount;
    form.querySelector('[name="description"]').value = transaction.description;
}

// Xử lý form submit
function handleTransactionSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);

    const transaction = {
        date: formData.get('date'),
        type: formData.get('type'),
        category: formData.get('category'),
        amount: parseFloat(formData.get('amount')),
        description: formData.get('description')
    };

    if (form.dataset.editId) {
        // Cập nhật giao dịch hiện có
        const id = parseInt(form.dataset.editId);
        const index = transactions.findIndex(t => t.id === id);
        if (index !== -1) {
            transactions[index] = { ...transactions[index], ...transaction };
        }
    } else {
        // Thêm giao dịch mới
        transaction.id = Date.now();
        transactions.unshift(transaction);
    }

    closeModal();
    applyFilters();
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Initialize when document is ready
document.addEventListener('DOMContentLoaded', initTransactionsPage);