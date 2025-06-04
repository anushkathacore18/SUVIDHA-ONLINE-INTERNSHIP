document.addEventListener('DOMContentLoaded', function () {
    // Update hidden role input when userType changes
    const radioButtons = document.querySelectorAll('input[name="userType"]');
    const roleInput = document.getElementById('role');
    const signupLink = document.getElementById('signup-link');
    const loginForm = document.querySelector('form');
    const usernameInput = document.querySelector('input[name="username"]');

    if (!roleInput || !signupLink || !loginForm || !usernameInput) {
        console.error('Required elements not found');
        return;
    }

    radioButtons.forEach(radio => {
        radio.addEventListener('change', function () {
            const selectedRole = this.value;
            roleInput.value = selectedRole;
            console.log("Selected role:", selectedRole);
        });
    });

    // Handle Sign Up link click
    signupLink.addEventListener('click', function (e) {
        e.preventDefault();
        const selectedRole = document.querySelector('input[name="userType"]:checked')?.value;
        if (!selectedRole) {
            console.error('No role selected');
            // Using a custom message box instead of alert()
            // You would implement a modal or a div to show this message
            const messageBox = document.createElement('div');
            messageBox.textContent = 'Please select a role (Student, Employee, or TPO).';
            messageBox.style.cssText = `
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background-color: #F8B400;
                color: white;
                padding: 15px 25px;
                border-radius: 8px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                z-index: 1000;
                font-size: 1.1em;
                animation: fadeOut 3s forwards; /* Reference the global keyframe */
            `;
            document.body.appendChild(messageBox);

            // No @keyframes definition here, it will be in CSS

            return;
        }
        window.location.href = `/register/${selectedRole}`;
    });

    // Optional: Client-side validation for username/email
    loginForm.addEventListener('submit', function (e) {
        const identifier = usernameInput.value.trim();
        // Simple regex to check if input is an email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const isEmail = emailRegex.test(identifier);
        const isUsername = /^[a-zA-Z0-9_]{3,}$/.test(identifier); // Example: username must be 3+ chars, alphanumeric or underscore

        if (!isEmail && !isUsername) {
            e.preventDefault();
            // Using a custom message box instead of alert()
            const messageBox = document.createElement('div');
            messageBox.textContent = 'Please enter a valid username (3+ characters, alphanumeric or underscore) or email address.';
            messageBox.style.cssText = `
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background-color: #D32F2F; /* Red for error */
                color: white;
                padding: 15px 25px;
                border-radius: 8px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                z-index: 1000;
                font-size: 1.1em;
                animation: fadeOut 3s forwards; /* Reference the global keyframe */
            `;
            document.body.appendChild(messageBox);

            // No @keyframes definition here, it will be in CSS
            
            return;
        }
    });

    // Button animation on click - REMOVED FOR THEME CONSISTENCY
    // The previous 'success-glow' animation was removed as it didn't align with the subtle theme.
    // The button's hover and active states are now handled purely by CSS transitions.
    const loginButton = document.querySelector('button');
    if (loginButton) {
        loginButton.addEventListener('click', function () {
            // No JavaScript animation needed, CSS handles hover/active states
            // Remove the following lines if they were present:
            // this.style.animation = 'success-glow 0.5s ease';
            // setTimeout(() => {
            //     this.style.animation = '';
            // }, 500);
        });
    }
});
