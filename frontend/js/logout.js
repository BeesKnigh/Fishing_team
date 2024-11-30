document.getElementById("logout-btn").addEventListener("click", function() {
    // Удаляем данные из localStorage
    localStorage.removeItem("userLogin");
    localStorage.removeItem("userPassword");

    // Перенаправляем пользователя на страницу входа
    window.location.href = "login.html";
});
