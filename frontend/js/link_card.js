document.addEventListener("DOMContentLoaded", function() {
    const linkCardForm = document.getElementById("link-card-form");
    const messageDiv = document.getElementById("card-message");

    linkCardForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Останавливаем стандартное поведение формы

        // Получаем данные из формы
        const cardExpiry = document.getElementById("card-expiry").value;
        const cardType = document.getElementById("card-type").value;
        const balance = document.getElementById("balance").value;

        // Проверка, что все данные введены
        if (!cardExpiry || !cardType || !balance) {
            messageDiv.textContent = "Пожалуйста, заполните все поля!";
            messageDiv.style.color = "red";
            return;
        }

        if (balance <= 0 || balance > 1000000) {
            messageDiv.textContent = "Баланс должен быть в пределах от 1 до 1 000 000!";
            messageDiv.style.color = "red";
            return;
        }

        // Запоминаем карту в localStorage
        const cardData = {
            cardExpiry: cardExpiry,
            cardType: cardType,
            balance: parseFloat(balance)
        };

        localStorage.setItem("linkedCard", JSON.stringify(cardData));

        // Показать успешное сообщение
        messageDiv.textContent = "Карта успешно привязана!";
        messageDiv.style.color = "#4CAF50"; // Зеленый цвет для успешного сообщения

        // Перенаправляем на страницу переводов
        setTimeout(function() {
            window.location.href = "transfers.html";
        }, 2000); // Переход через 2 секунды
    });
});
