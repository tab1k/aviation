const showBtn = document.querySelector('.show-more');

function showMoreStudents() {
    const studentsItems = document.querySelectorAll('.students__item');
    const arr = Array.from(studentsItems);
    const showedStudents = arr.filter((student) => student.classList.contains('show'));

    if (arr.length === showedStudents.length) {
        showBtn.disabled = 'true';
    } else {
        for (let i = showedStudents.length; i < showedStudents.length + 9; i++) {
            studentsItems[i].classList.add('show');
        }
    }
}

showBtn.addEventListener('click', showMoreStudents);