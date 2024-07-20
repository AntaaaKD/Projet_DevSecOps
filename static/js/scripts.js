document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.querySelector('#signup form');
    const loginForm = document.querySelector('#login form');

    signupForm.addEventListener('submit', (e) => {
        e.preventDefault();
        if (validateForm(signupForm)) {
            alert('Inscription réussie!');
            // Ici, vous pouvez ajouter la logique pour gérer l'inscription
        }
    });

    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        if (validateForm(loginForm)) {
            alert('Connexion réussie!');
            // Ici, vous pouvez ajouter la logique pour gérer la connexion
        }
    });

    function validateForm(form) {
        let valid = true;
        form.querySelectorAll('input').forEach(input => {
            if (!input.value) {
                valid = false;
                input.classList.add('invalid');
            } else {
                input.classList.remove('invalid');
            }
        });
        return valid;
    }

    // Ajoute des transitions douces entre les sections
    document.querySelectorAll('.hero a').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});
