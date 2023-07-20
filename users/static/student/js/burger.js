var burgerContent = document.querySelector('.burger-content');

function toggleBurgerContent() {
  if (burgerContent.style.left === '-100%') {
    burgerContent.style.left = '0%';
  } else {
    burgerContent.style.left = '-100%';
  }
}