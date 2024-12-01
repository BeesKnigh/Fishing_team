document.addEventListener("DOMContentLoaded", function() {
    // Получаем логин пользователя из localStorage
    const userLogin = localStorage.getItem("userLogin");

    // Проверяем, есть ли логин, если нет, перенаправляем на страницу входа
    if (!userLogin) {
        window.location.href = "login.html";
    } else {
        // Если логин найден, отображаем его на странице
        document.getElementById("user-name").textContent = userLogin;
    }

    // Обработчик для кнопки "Переводы"
    document.getElementById("transfers-btn").addEventListener("click", function() {
        window.location.href = "transfers.html";
    });

    // Обработчик для кнопки "Выйти"
    document.getElementById("logout-btn").addEventListener("click", async function() {
        const token = localStorage.getItem("access_token");  // Получаем токен из localStorage

        if (!token) {
            // Если токен не найден, перенаправляем на страницу входа
            window.location.href = "login.html";
            return;
        }

        // Отправляем запрос на сервер для выхода
        try {
            const response = await fetch("http://localhost:8000/logout", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            });

            if (response.ok) {
                // Если выход успешен, удаляем данные из localStorage
                localStorage.removeItem("userLogin");
                localStorage.removeItem("access_token");
                window.location.href = "login.html";  // Перенаправляем на страницу входа
            } else {
                // Если произошла ошибка, выводим сообщение об ошибке
                const errorData = await response.json();
                alert(`Ошибка: ${errorData.detail}`);
            }
        } catch (error) {
            console.error("Ошибка при выходе из системы:", error);
            alert("Не удалось выйти. Попробуйте еще раз.");
        }
    });
});
