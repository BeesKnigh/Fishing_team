
const loginForm = document.getElementById('login-form');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const errorMessage = document.getElementById('error-message');


loginForm.addEventListener('submit', function(event) {
    event.preventDefault(); 

    const email = emailInput.value;
    const password = passwordInput.value;

    
    if (!email || !password) {
        errorMessage.textContent = 'Пожалуйста, заполните все поля!';
        return;
    }

    
    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            password: password,
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Ошибка авторизации');
        }
        return response.json();
    })
    .then(data => {
       
        if (data.success) {
           
            window.location.href = '/dashboard.html';  
        } else {
           
            errorMessage.textContent = 'Неверный логин или пароль.';
        }
    })
    .catch(error => {
        errorMessage.textContent = 'Произошла ошибка: ' + error.message;
    });
});
