function initSettingsPage() {
    initializeImageUpload();
    initializeFormValidation();
    initializeToggles();
}

function initializeImageUpload() {
    const imageUpload = document.getElementById('imageUpload');
    const profileImage = document.getElementById('profileImage');

    imageUpload.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                profileImage.src = e.target.result;
            }
            reader.readAsDataURL(file);
        }
    });
}

function initializeFormValidation() {
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    const emailInput = document.getElementById('email');

    // Password validation
    passwordInputs.forEach(input => {
        input.addEventListener('input', validatePassword);
    });

    // Email validation
    emailInput.addEventListener('input', validateEmail);
}

function validatePassword() {
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (newPassword && confirmPassword && newPassword !== confirmPassword) {
        document.getElementById('confirmPassword').setCustomValidity("Passwords don't match");
    } else {
        document.getElementById('confirmPassword').setCustomValidity('');
    }
}

function validateEmail(e) {
    const email = e.target.value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (!emailRegex.test(email)) {
        e.target.setCustomValidity('Please enter a valid email address');
    } else {
        e.target.setCustomValidity('');
    }
}

function saveAllSettings() {
    // Collect all settings
    const settings = {
        profile: {
            fullName: document.getElementById('fullName').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value
        },
        preferences: {
            currency: document.getElementById('currency').value,
            language: document.getElementById('language').value,
            notifications: {
                email: document.querySelector('.notification-preferences input:nth-child(1)').checked,
                push: document.querySelector('.notification-preferences input:nth-child(2)').checked,
                budget: document.querySelector('.notification-preferences input:nth-child(3)').checked
            }
        },
        security: {
            twoFactor: document.querySelector('.security-options input:nth-child(1)').checked,
            faceId: document.querySelector('.security-options input:nth-child(2)').checked
        }
    };

    // Save to backend (mock for now)
    console.log('Saving settings:', settings);
    showSaveConfirmation();
}

function showSaveConfirmation() {
    // Create and show notification
    const notification = document.createElement('div');
    notification.className = 'save-notification';
    notification.innerHTML = `
        <i class="fas fa-check-circle"></i>
        Settings saved successfully
    `;
    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Add this to the existing style block or create a new one
const style = document.createElement('style');
style.textContent = `
    .save-notification {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #4CAF50;
        color: white;
        padding: 15px 25px;
        border-radius: 5px;
        display: flex;
        align-items: center;
        gap: 10px;
        animation: slideIn 0.3s ease-out;
    }

    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);