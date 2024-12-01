document.addEventListener("DOMContentLoaded", function() {
    const transferForm = document.getElementById("transfer-form");
    const messageDiv = document.getElementById("message");

    // Получаем данные из localStorage
    const linkedCard = JSON.parse(localStorage.getItem("linkedCard"));

    // Если карта привязана, показываем её данные
    if (linkedCard) {
        const senderCardField = document.getElementById("sender-card");
        senderCardField.value = `Тип карты: ${linkedCard.cardType}, Баланс: ${linkedCard.balance} руб.`;
    }

    transferForm.addEventListener("submit", async function(event) {
        event.preventDefault(); // Отменяем стандартную отправку формы

        // Получаем значения из формы
        const operType = document.getElementById("oper_type").value;
        const sum = document.getElementById("sum").value;
        const pinIncCount = document.getElementById("pin_inc_count").value;

        // Проверяем, что все данные введены корректно
        if (!linkedCard) {
            messageDiv.textContent = "Ошибка: карта не привязана!";
            messageDiv.style.color = "red";
            return;
        }

        if (sum <= 0) {
            messageDiv.textContent = "Сумма операции должна быть больше нуля.";
            messageDiv.style.color = "red";
            return;
        }

        if (pinIncCount < 0) {
            messageDiv.textContent = "Количество неверных попыток не может быть отрицательным.";
            messageDiv.style.color = "red";
            return;
        }

        try {
            // Отправляем данные о транзакции на сервер
            const response = await fetch('http://localhost:8000/transactions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem("access_token")}`,  // Используем токен из localStorage
                },
                body: JSON.stringify({
                    oper_type: operType,
                    sum: sum,
                    pin_inc_count: pinIncCount,
                    client_id: linkedCard.clientId,  // ID клиента (можно хранить в linkedCard)
                    card_type: linkedCard.cardType,  // Тип карты
                    card_status: linkedCard.cardStatus,  // Статус карты
                    expiration_date: linkedCard.expirationDate,  // Дата окончания карты
                }),
            });

            if (response.ok) {
                // Если транзакция успешна
                messageDiv.textContent = `Транзакция успешно проведена: ${operType}, сумма: ${sum} руб.`;
                messageDiv.style.color = "#4CAF50"; // Зеленый цвет для успешного сообщения
                transferForm.reset();
            } else {
                const errorData = await response.json();
                messageDiv.textContent = errorData.detail || "Ошибка при проведении транзакции.";
                messageDiv.style.color = "red";
            }
        } catch (error) {
            console.error("Ошибка при проведении транзакции:", error);
            messageDiv.textContent = "Ошибка соединения с сервером.";
            messageDiv.style.color = "red";
        }
    });
});

