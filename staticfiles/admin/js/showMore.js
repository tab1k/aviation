// const showBtn = document.querySelector('.show-more');

// function showMoreStudents() {
//     const studentsItems = document.querySelectorAll('.students__item');
//     const arr = Array.from(studentsItems);
//     const showedStudents = arr.filter((student) => student.classList.contains('show'));

//     if (arr.length === showedStudents.length) {
//         showBtn.disabled = 'true';
//     } else {
//         for (let i = showedStudents.length; i < showedStudents.length + 9; i++) {
//             studentsItems[i].classList.add('show');
//         }
//     }
// }

// showBtn.addEventListener('click', showMoreStudents);



let button = document.querySelector('.show-more');
let elements = document.querySelectorAll('.students__item');
let content = document.querySelector('.students__content');
let elementHeight = elements[0].innerHeight;
let maxHeight = content.offsetHeight;

if (window.innerWidth < 850) {
  elementHeight = 250;

  maxHeight = elementHeight * 9;
  content.style.maxHeight = maxHeight + 'px';
} else {
  elementHeight = 60;
  maxHeight = elementHeight * 9 - 5;
  content.style.maxHeight = maxHeight + 'px';
}

button.addEventListener('click', function() {

  if (content.offsetHeight < maxHeight) {
    button.disabled = "true";
  } else {
    maxHeight += elementHeight * 9;
    content.style.maxHeight = maxHeight + 'px';
  }
});