let budgetData = {
    total: 5000,
    spent: 3240,
    remaining: 1760,
    categories: [
        {
            name: 'Shopping',
            icon: 'fa-shopping-bag',
            budget: 1000,
            spent: 800,
            color: '#3498db'
        },
        {
            name: 'Food',
            icon: 'fa-utensils',
            budget: 600,
            spent: 450,
            color: '#e74c3c'
        }
        // Add more categories as needed
    ]
};

function initBudgetPage() {
    updateBudgetOverview();
    renderBudgetCards();
    initializeBudgetModal();
}

function updateBudgetOverview() {
    const overviewItems = document.querySelectorAll('.overview-item');
    overviewItems[0].querySelector('.amount').textContent = `$${budgetData.total}`;
    overviewItems[1].querySelector('.amount').textContent = `$${budgetData.spent}`;
    overviewItems[2].querySelector('.amount').textContent = `$${budgetData.remaining}`;
}

function renderBudgetCards() {
    const budgetGrid = document.querySelector('.budget-grid');
    budgetGrid.innerHTML = budgetData.categories.map(category => {
        const percentage = (category.spent / category.budget) * 100;
        return `
            <div class="budget-card">
                <div class="budget-header">
                    <div class="category-icon" style="background: ${category.color}">
                        <i class="fas ${category.icon}"></i>
                    </div>
                    <div class="category-info">
                        <h3>${category.name}</h3>
                        <p>$${category.spent} / $${category.budget}</p>
                    </div>
                    <div class="category-actions">
                        <button class="btn-edit" onclick="editBudget('${category.name}')">
                            <i class="fas fa-edit"></i>
                        </button>
                    </div>
                </div>
                <div class="progress-container">
                    <div class="progress-bar">
                        <div class="progress" style="width: ${percentage}%;"></div>
                    </div>
                    <span class="progress-text ${percentage > 75 ? 'warning' : ''}">${percentage}%</span>
                </div>
            </div>
        `;
    }).join('');
}

function initializeBudgetModal() {
    const modal = document.getElementById('budgetModal');
    const addButton = document.querySelector('.btn-add');
    const closeBtn = document.querySelector('.close');
    const cancelBtn = document.querySelector('.btn-cancel');

    addButton.addEventListener('click', () => {
        modal.style.display = 'block';
    });

    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    cancelBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    document.getElementById('budgetForm').addEventListener('submit', handleBudgetSubmit);
}

function handleBudgetSubmit(e) {
    e.preventDefault();
    // Handle form submission
    const formData = new FormData(e.target);
    const category = formData.get('category');
    const amount = parseFloat(formData.get('amount'));
    const period = formData.get('period');

    // Update budget data
    updateBudgetData(category, amount, period);

    // Close modal
    document.getElementById('budgetModal').style.display = 'none';
}

function editBudget(categoryName) {
    const category = budgetData.categories.find(c => c.name === categoryName);
    if (!category) return;

    const modal = document.getElementById('budgetModal');
    modal.style.display = 'block';
    
    // Pre-fill form with category data
    const form = document.getElementById('budgetForm');
    form.querySelector('select[name="category"]').value = categoryName.toLowerCase();
    form.querySelector('input[name="amount"]').value = category.budget;
}