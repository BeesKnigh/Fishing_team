document.addEventListener("DOMContentLoaded", function() {
    // Получаем логин пользователя из localStorage
    const userLogin = localStorage.getItem("userLogin");

    // Если логин найден, отображаем его на странице
    if (userLogin) {
        document.getElementById("user-name").textContent = userLogin;
    } else {
        // Если логин не найден, перенаправляем на страницу входа
        window.location.href = "login.html";
    }

    // Обработчик для кнопки "Переводы"
    document.getElementById("transfers-btn").addEventListener("click", function() {
        window.location.href = "transfers.html";
    });

    // Обработчик для кнопки "Выйти"
    document.getElementById("logout-btn").addEventListener("click", function() {
        localStorage.removeItem("userLogin");  // Удаляем логин из localStorage
        window.location.href = "login.html";   // Перенаправляем на страницу входа
    });
});
