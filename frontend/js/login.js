const loginForm = document.getElementById("login-form");
const errorMessage = document.getElementById("error-message");

loginForm.addEventListener("submit", async function(event) {
    event.preventDefault();  // Останавливаем стандартную отправку формы

    const login = document.getElementById("login").value;
    const password = document.getElementById("password").value;

    try {
        // Отправляем запрос на бэкенд для получения токена
        const response = await fetch('http://localhost:8000/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                username: login,
                password: password,
            }),
        });

        if (response.ok) {
            const data = await response.json();
            const token = data.access_token;
            localStorage.setItem("access_token", token);  // Сохраняем токен в localStorage
            localStorage.setItem("userLogin", login);  // Сохраняем логин в localStorage

            // Перенаправляем на страницу профиля
            window.location.href = "profile.html";
        } else {
            errorMessage.textContent = "Неверный логин или пароль.";
            errorMessage.style.color = "red";
        }
    } catch (error) {
        console.error("Ошибка при входе:", error);
        errorMessage.textContent = "Ошибка соединения с сервером.";
        errorMessage.style.color = "red";
    }
});
