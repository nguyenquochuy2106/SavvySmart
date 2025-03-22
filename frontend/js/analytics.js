// Thêm biến toàn cục để lưu các biểu đồ
let trendChart;
let pieChart;

function initAnalyticsPage() {
    console.log('Initializing Analytics Page');
    try {
        initializePieChart();
        console.log('Pie Chart initialized');
        initializeTrendChart();
        console.log('Trend Chart initialized');
        initializePeriodSelector();
        console.log('Period Selector initialized');
        loadTopSpendingCategories();
        console.log('Top Categories loaded');
    } catch (error) {
        console.error('Error initializing analytics:', error);
    }
}

function initializePieChart() {
    const ctx = document.getElementById('categoryPieChart').getContext('2d');
    pieChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Shopping', 'Food', 'Transport', 'Entertainment', 'Bills'],
            datasets: [{
                data: [2500, 1800, 1200, 900, 1900],
                backgroundColor: [
                    '#2ecc71',
                    '#3498db',
                    '#e74c3c',
                    '#f1c40f',
                    '#9b59b6'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true, // Thêm option này
            aspectRatio: 1, // Tỷ lệ 1:1
            plugins: {
                legend: {
                    position: 'right',
                    align: 'center'
                }
            },
            layout: {
                padding: {
                    left: 10,
                    right: 10,
                    top: 10,
                    bottom: 10
                }
            }
        }
    });
}

function initializeTrendChart() {
    const ctx = document.getElementById('trendLineChart').getContext('2d');
    trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Income',
                data: [3000, 3500, 2900, 3300, 3200, 3800],
                borderColor: '#2ecc71',
                tension: 0.4
            }, {
                label: 'Expenses',
                data: [2500, 2300, 2800, 2600, 2400, 2900],
                borderColor: '#e74c3c',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top'
                }
            }
        }
    });
}

// Thêm hàm updateTrendChart
function updateTrendChart(data) {
    if (!trendChart) return;

    let labels;
    switch (data.period) {
        case 'month':
            labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
            break;
        case 'quarter':
            labels = ['Q1', 'Q2', 'Q3', 'Q4'];
            break;
        case 'year':
            labels = ['2021', '2022', '2023', '2024'];
            break;
        default:
            labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
    }

    trendChart.data.labels = labels;
    trendChart.data.datasets[0].data = data.income;
    trendChart.data.datasets[1].data = data.expenses;
    trendChart.update();
}

function initializePeriodSelector() {
    const periodButtons = document.querySelectorAll('.period-btn');
    periodButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            periodButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            button.classList.add('active');
            // Update charts based on selected period
            updateChartsForPeriod(button.dataset.period);
        });
    });
}

function updateChartsForPeriod(period) {
    // Mock data - In real application, this would fetch data from backend
    const mockData = {
        month: {
            period: 'month',
            income: [3000, 3500, 2900, 3300, 3200, 3800],
            expenses: [2500, 2300, 2800, 2600, 2400, 2900]
        },
        quarter: {
            period: 'quarter',
            income: [9400, 9800, 10300, 11200],
            expenses: [7600, 8100, 8500, 8900]
        },
        year: {
            period: 'year',
            income: [38000, 42000, 45000, 48000],
            expenses: [31000, 34000, 36000, 38000]
        }
    };

    // Update charts with new data
    updateTrendChart(mockData[period]);
}

function loadTopSpendingCategories() {
    const categories = [
        { name: 'Shopping', amount: 2500, percentage: 75 },
        { name: 'Food', amount: 1800, percentage: 60 },
        { name: 'Transport', amount: 1200, percentage: 40 },
        { name: 'Entertainment', amount: 900, percentage: 30 }
    ];

    const categoryList = document.querySelector('.category-list');
    categoryList.innerHTML = categories.map(category => `
        <div class="category-item">
            <div class="category-info">
                <span class="category-name">${category.name}</span>
                <span class="category-amount">$${category.amount}</span>
            </div>
            <div class="progress-bar">
                <div class="progress" style="width: ${category.percentage}%;"></div>
            </div>
        </div>
    `).join('');
}