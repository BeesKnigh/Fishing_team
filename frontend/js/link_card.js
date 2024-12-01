document.addEventListener("DOMContentLoaded", function() {
    const linkCardForm = document.getElementById("link-card-form");
    const messageDiv = document.getElementById("card-message");

    // Получаем access_token из localStorage
    const accessToken = localStorage.getItem("access_token");

    // Если токен не найден, перенаправляем на страницу входа
    if (!accessToken) {
        window.location.href = "login.html";  // Перенаправление на страницу входа
        return;
    }

    linkCardForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Останавливаем стандартное поведение формы

        // Получаем данные из формы
        const cardExpiry = document.getElementById("card-expiry").value;
        const cardType = document.getElementById("card-type").value;
        const balance = parseFloat(document.getElementById("balance").value);

        // Проверка, что все данные введены
        if (!cardExpiry || !cardType || !balance) {
            messageDiv.textContent = "Пожалуйста, заполните все поля!";
            messageDiv.style.color = "red";
            return;
        }

        // Проверка баланса
        if (balance <= 0 || balance > 1000000) {
            messageDiv.textContent = "Баланс должен быть в пределах от 1 до 1 000 000!";
            messageDiv.style.color = "red";
            return;
        }

        // Создаем объект с данными карты
        const cardData = {
            card_type: cardType,
            card_status: "active",  // Пример статуса карты
            expiration_date: cardExpiry,  // Дата в формате YYYY-MM-DD
            balance: balance,
            client_id: 1  // Здесь нужно передать реальный client_id, если он известен
        };

        // Отправляем данные на сервер
        fetch("http://localhost:8000/cards", {  // Используем правильный абсолютный URL для вашего сервера
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`  // Отправляем токен в заголовке
            },
            body: JSON.stringify(cardData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Ошибка при привязке карты");
            }
            return response.json();
        })
        .then(data => {
            // Если карта успешно привязана, показываем сообщение
            messageDiv.textContent = "Карта успешно привязана!";
            messageDiv.style.color = "#4CAF50"; // Зеленый цвет для успешного сообщения

            // Перенаправляем на страницу переводов
            setTimeout(function() {
                window.location.href = "transfers.html";
            }, 2000); // Переход через 2 секунды
        })
        .catch(error => {
            messageDiv.textContent = `Ошибка: ${error.message}`;
            messageDiv.style.color = "red";
        });
    });
});
