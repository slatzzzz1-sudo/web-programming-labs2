function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        for(let i = 0; i<films.length; i++) {
            let tr = document.createElement('tr');

            let tdTitle = document.createElement('td');
            let tdTitleRus = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdAction = document.createElement('td');

            tdTitle.innerHTML = films[i].title === films[i].title_ru ? '' : films[i].title;
            tdTitleRus.innerHTML = films[i].title_rus;
            tdYear.innerText = films[i].year;

            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';

            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';

            tdAction.appendChild(editButton);
            tdAction.appendChild(delButton);

            tr.appendChild(tdTitle);
            tr.appendChild(tdTitleRus);
            tr.appendChild(tdYear);
            tr.appendChild(tdAction);

            tbody.appendChild(tr);
        }
    })
}