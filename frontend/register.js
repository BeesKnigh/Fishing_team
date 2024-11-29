// Получаем элементы формы
const registerForm = document.getElementById('register-form');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confirm-password');
const errorMessage = document.getElementById('error-message');

// Обработчик события на форму
registerForm.addEventListener('submit', function(event) {
    event.preventDefault();  // Отменяем стандартное поведение формы

    // Получаем значения из формы
    const email = emailInput.value;
    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;

    // Проверка на совпадение паролей
    if (password !== confirmPassword) {
        errorMessage.textContent = 'Пароли не совпадают!';
        return;
    }

    // Отправка данных на сервер через Fetch API
    fetch('/api/register', {
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
            throw new Error('Ошибка регистрации');
        }
        return response.json();
    })
    .then(data => {
        // Если сервер вернул успешный ответ
        if (data.success) {
            // Перенаправляем на страницу входа
            window.location.href = '/login.html';
        } else {
            // Показываем ошибку
            errorMessage.textContent = data.message || 'Неизвестная ошибка';
        }
    })
    .catch(error => {
        errorMessage.textContent = 'Произошла ошибка: ' + error.message;
    });
});
