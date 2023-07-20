const button = document.querySelector(".button");

function verified() {
    if (button.classList.contains('verified')) {
        button.classList.remove('verified');
        button.textContent = "Ожидает проверку";
    } else {
        button.classList.add('verified');
        button.textContent = "Проверено";
    }
}

button.addEventListener('click', verified);

