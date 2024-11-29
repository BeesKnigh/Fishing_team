document.getElementById('login-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const login = document.getElementById('login').value;
    const password = document.getElementById('password').value;

    // Здесь можно отправить запрос на сервер
    // Например:
    // fetch('/login', {
    //     method: 'POST',
    //     body: JSON.stringify({ login, password }),
    //     headers: { 'Content-Type': 'application/json' }
    // })
    // .then(response => response.json())
    // .then(data => {
    //     if (data.success) {
    //         window.location.href = 'dashboard.html'; // Перенаправление на страницу после успешного входа
    //     } else {
    //         document.getElementById('error-message').textContent = 'Неверный логин или пароль';
    //     }
    // });
});
