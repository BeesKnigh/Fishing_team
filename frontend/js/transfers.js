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

    transferForm.addEventListener("submit", function(event) {
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

        // Логика успешной транзакции
        messageDiv.textContent = `Транзакция: ${operType}, сумма: ${sum} руб.`;
        messageDiv.style.color = "#4CAF50"; // Зеленый цвет для успешного сообщения

        // Очистить поля формы после успешного перевода
        transferForm.reset();
    });
});
