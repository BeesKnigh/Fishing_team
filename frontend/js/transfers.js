document.addEventListener("DOMContentLoaded", function() {
    const transferForm = document.getElementById("transfer-form");
    const messageDiv = document.getElementById("message");

    // Пример того, как можно заполнять данные о привязанной карте (можно заменить на реальный API)
    const storedCard = localStorage.getItem('linkedCard') || null;
    const senderCardField = document.getElementById("sender-card");

    // Проверка привязанной карты
    if (storedCard) {
        senderCardField.value = storedCard;
    } else {
        senderCardField.value = 'Карта не привязана';
    }

    transferForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Отменяем стандартную отправку формы

        // Если карта не привязана
        if (!storedCard) {
            messageDiv.textContent = "Для выполнения операции необходимо привязать карту.";
            messageDiv.style.color = "red";
            return;
        }

        // Получаем значения из формы
        const operType = document.getElementById("oper_type").value;
        const deviceType = document.getElementById("device_type").value;
        const cardType = document.getElementById("card_type").value;
        const tranCode = document.getElementById("tran_code").value;
        const balance = parseFloat(document.getElementById("balance").value);
        const sum = parseFloat(document.getElementById("sum").value);
        const pinIncCount = parseInt(document.getElementById("pin_inc_count").value, 10);

        // Проверка валидности баланса и суммы
        if (isNaN(balance) || isNaN(sum) || balance < 0 || sum < 1 || balance > 1000000 || sum > 1000000) {
            messageDiv.textContent = "Баланс и сумма должны быть положительными числами и не более 1 миллиона.";
            messageDiv.style.color = "red";
            return;
        }

        if (sum > balance) {
            messageDiv.textContent = "Недостаточно средств на балансе для выполнения операции.";
            messageDiv.style.color = "red";
            return;
        }

        if (pinIncCount < 0) {
            messageDiv.textContent = "Количество неверных попыток не может быть отрицательным.";
            messageDiv.style.color = "red";
            return;
        }

        // Логика успешной транзакции
        messageDiv.textContent = `Операция: ${operType}, Тип устройства: ${deviceType}, Тип карты: ${cardType}, Код трансфера: ${tranCode}, Баланс: ${balance.toFixed(2)}, Сумма: ${sum.toFixed(2)}`;
        messageDiv.style.color = "#4CAF50"; // Зеленый цвет для успешного сообщения

        // Очистить поля формы после успешного перевода
        transferForm.reset();
    });
});
