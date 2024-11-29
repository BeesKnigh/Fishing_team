document.getElementById('register-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const login = document.getElementById('login').value;
    const password = document.getElementById('password').value;

    // Здесь можно отправить запрос на сервер для регистрации
    // Например:
    // fetch('/register', {
    //     method: 'POST',
    //     body: JSON.stringify({ login, password }),
    //     headers: { 'Content-Type': 'application/json' }
    // })
    // .then(response => response.json())
    // .then(data => {
    //     if (data.success) {
    //         window.location.href = 'login.html'; // Перенаправление на страницу входа
    //     } else {
    //         document.getElementById('error-message').textContent = 'Ошибка регистрации';
    //     }
    // });
});
