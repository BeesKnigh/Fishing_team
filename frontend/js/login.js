// Получаем элементы формы входа
const loginForm = document.getElementById("login-form");
const errorMessage = document.getElementById("error-message");

// Обработчик отправки формы входа
loginForm.addEventListener("submit", function(event) {
    event.preventDefault();  // Останавливаем стандартную отправку формы

    // Получаем введенные значения логина и пароля
    const login = document.getElementById("login").value;
    const password = document.getElementById("password").value;

    // Получаем сохраненные значения из localStorage
    const storedLogin = localStorage.getItem("userLogin");
    const storedPassword = localStorage.getItem("userPassword");

    // Проверяем, совпадают ли логин и пароль
    if (login === storedLogin && password === storedPassword) {
        // Перенаправляем на профиль, если данные верные
        window.location.href = "profile.html";  // Профиль или другая страница
    } else {
        // Если данные неверные, показываем ошибку
        errorMessage.textContent = "Неверный логин или пароль.";
        errorMessage.style.color = "red";
    }
});
