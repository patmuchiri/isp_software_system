document.addEventListener('DOMContentLoaded', () => {
    // Example: Smooth scroll to sections
    const links = document.querySelectorAll('a[href^="#"]');
    for (const link of links) {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            document.getElementById(targetId).scrollIntoView({
                behavior: 'smooth'
            });
        });
    }

    // Example: Form validation
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', (e) => {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            if (username === '' || password === '') {
                e.preventDefault();
                alert('Please fill in both fields.');
            }
        });
    }
});
