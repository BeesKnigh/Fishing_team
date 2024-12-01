// Получаем элементы формы
const registerForm = document.getElementById("register-form");
const errorMessage = document.getElementById("error-message");

// Обработчик отправки формы регистрации
registerForm.addEventListener("submit", async function(event) {
    event.preventDefault();  // Останавливаем стандартную отправку формы

    // Получаем значения логина и пароля
    const login = document.getElementById("login").value;
    const password = document.getElementById("password").value;

    if (login && password) {
        try {
            // Отправляем данные на сервер для регистрации
            const response = await fetch('http://localhost:8000/clients', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: login,
                    client_pas: password,  // Пароль, который будет сохранен на сервере
                }),
            });

            if (response.ok) {
                // Если регистрация успешна, оповещаем пользователя
                alert("Вы успешно зарегистрированы!");

                // Перенаправляем на страницу входа
                window.location.href = "login.html";  // или другой путь, если требуется
            } else {
                const errorData = await response.json();
                errorMessage.textContent = errorData.detail || "Ошибка при регистрации.";
                errorMessage.style.color = "red";
            }
        } catch (error) {
            console.error("Ошибка при регистрации:", error);
            errorMessage.textContent = "Ошибка соединения с сервером.";
            errorMessage.style.color = "red";
        }
    }
});
