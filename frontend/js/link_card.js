document.addEventListener("DOMContentLoaded", function() {
    const linkCardForm = document.getElementById("link-card-form");
    const cardNumberInput = document.getElementById("card-number");
    const cardExpiryInput = document.getElementById("card-expiry");
    const cardCvcInput = document.getElementById("card-cvc");
    const messageDiv = document.getElementById("card-message");

    // Проверка, если карта уже привязана
    if (localStorage.getItem('linkedCard')) {
        messageDiv.textContent = "Карта уже привязана.";
        messageDiv.style.color = "green";
    }

    linkCardForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Отменяем стандартное поведение формы

        const cardNumber = cardNumberInput.value.trim();
        const cardExpiry = cardExpiryInput.value.trim();
        const cardCvc = cardCvcInput.value.trim();

        // Проверяем, чтобы все поля были заполнены
        if (!cardNumber || !cardExpiry || !cardCvc) {
            messageDiv.textContent = "Пожалуйста, заполните все поля.";
            messageDiv.style.color = "red";
            return;
        }

        // Сохраняем привязанную карту в localStorage
        const cardData = {
            cardNumber: cardNumber,
            cardExpiry: cardExpiry,
            cardCvc: cardCvc
        };

        localStorage.setItem('linkedCard', JSON.stringify(cardData));

        // Выводим сообщение об успешной привязке
        messageDiv.textContent = "Карта успешно привязана!";
        messageDiv.style.color = "green";

        // Перенаправляем на страницу переводов после привязки
        setTimeout(function() {
            window.location.href = "transfers.html"; // Перенаправление на страницу переводов
        }, 2000); // 2 секунды задержки для показа сообщения
    });
});
