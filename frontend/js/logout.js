document.getElementById("logout-btn").addEventListener("click", function() {
    // Удаляем данные из localStorage
    localStorage.removeItem("userLogin");
    localStorage.removeItem("userPassword");
    localStorage.removeItem("accessToken");  // Удаляем токен доступа

    // Отправляем запрос на сервер для завершения сессии (опционально)
    const accessToken = localStorage.getItem("accessToken");

    if (accessToken) {
        fetch("/logout", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${accessToken}`  // Отправляем токен в заголовке
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Ошибка при выходе");
            }
            // После успешного выхода перенаправляем на страницу входа
            window.location.href = "login.html";
        })
        .catch(error => {
            console.error("Ошибка при выходе:", error);
            // Даже если не удалось выполнить запрос на сервер, удаляем локальные данные
            window.location.href = "login.html";  // Перенаправляем на страницу входа
        });
    } else {
        // Если нет токена, просто перенаправляем на страницу входа
        window.location.href = "login.html";
    }
});
