// Thêm biến lưu trữ nội dung dashboard
let originalDashboardContent = '';

document.addEventListener('DOMContentLoaded', function() {
    // Lưu nội dung dashboard ban đầu
    originalDashboardContent = document.querySelector('.main-content').innerHTML;

    // Khởi tạo biểu đồ
    initializeChart();

    // Get all navigation items
    const navItems = document.querySelectorAll('.nav-links li');
    
    // Add click event to each nav item
    navItems.forEach(item => {
        item.addEventListener('click', async function() {
            // Remove active class from all items
            navItems.forEach(nav => nav.classList.remove('active'));
            
            // Add active class to clicked item
            this.classList.add('active');
            
            // Get page name from data attribute
            const page = this.getAttribute('data-page');
            
            if (page === 'dashboard') {
                // Load original dashboard content
                loadDashboardContent();
            } else {
                // Load other pages
                await loadPage(page);
            }
        });
    });
});

// Tách hàm khởi tạo biểu đồ
function initializeChart() {
    const ctx = document.getElementById('monthlyChart').getContext('2d');
    new Chart(ctx, {
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
                    position: 'top',
                }
            }
        }
    });
}

function loadDashboardContent() {
    // Khôi phục nội dung dashboard gốc
    document.querySelector('.main-content').innerHTML = originalDashboardContent;
    // Khởi tạo lại biểu đồ vì element đã được thay thế
    initializeChart();
}

async function loadPage(pageName) {
    try {
        const response = await fetch(`../pages/${pageName}.html`);
        const content = await response.text();
        
        // Insert the new content
        document.querySelector('.main-content').innerHTML = content;
        
        // Initialize any scripts needed for the new page
        initializePageScripts(pageName);
    } catch (error) {
        console.error('Error loading page:', error);
    }
}

function initializePageScripts(pageName) {
    switch(pageName) {
        case 'transactions':
            initTransactionsPage();
            break;
        case 'analytics':
            console.log('Loading analytics page');
            if (typeof initAnalyticsPage === 'undefined') {
                // Load analytics.js if not already loaded
                const script = document.createElement('script');
                script.src = '../js/analytics.js';
                script.onload = () => {
                    console.log('Analytics.js loaded');
                    initAnalyticsPage();
                };
                document.head.appendChild(script);
            } else {
                initAnalyticsPage();
            }
            break;
        case 'budget':
            if (typeof initBudgetPage === 'undefined') {
                const script = document.createElement('script');
                script.src = '../js/budget.js';
                script.onload = () => {
                    console.log('Budget.js loaded');
                    initBudgetPage();
                };
                document.head.appendChild(script);
            } else {
                initBudgetPage();
            }
            break;
        case 'settings':
            if (typeof initSettingsPage === 'undefined') {
                const script = document.createElement('script');
                script.src = '../js/settings.js';
                script.onload = () => {
                    console.log('Settings.js loaded');
                    initSettingsPage();
                };
                document.head.appendChild(script);
            } else {
                initSettingsPage();
            }
            break;
        // Add other page initializations as needed
    }
}

function initTransactionsPage() {
    // Initialize transaction page specific functions
    const addButton = document.querySelector('.btn-add');
    const modal = document.getElementById('transactionModal');
    const closeBtn = document.querySelector('.close');
    
    addButton?.addEventListener('click', () => {
        modal.style.display = "block";
    });
    
    closeBtn?.addEventListener('click', () => {
        modal.style.display = "none";
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });
}

// Notifications handling
document.querySelector('.fa-bell').addEventListener('click', function() {
    // Add notification logic here
});

// Search functionality
document.querySelector('.search-bar input').addEventListener('input', function(e) {
    // Add search logic here
});