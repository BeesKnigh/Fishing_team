// Получаем элементы формы
const registerForm = document.getElementById("register-form");

// Обработчик отправки формы регистрации
registerForm.addEventListener("submit", function(event) {
    event.preventDefault();  // Останавливаем стандартную отправку формы

    // Получаем значения логина и пароля
    const login = document.getElementById("login").value;
    const password = document.getElementById("password").value;

    // Сохраняем логин и пароль в localStorage
    if (login && password) {
        localStorage.setItem("userLogin", login);
        localStorage.setItem("userPassword", password);

        // Оповещаем пользователя об успешной регистрации
        alert("Вы успешно зарегистрированы!");

        // Перенаправляем на страницу входа
        window.location.href = "login.html";  // или другой путь, если требуется
    }
});
