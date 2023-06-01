function statusTravel(my_url, status_choice, status_name) {
    let token = document.querySelector('#p-token');
    fetch(
        my_url,
        {
            method: 'PATCH', headers: {"X-CSRFToken": token.innerText, 'Content-type': 'application/json'},
            body: JSON.stringify({status: status_choice})
        }
    )
        .then(
            function (resp) {
                if (!resp.ok) {
                    alert('Wystąpił błąd! Otwórz devtools i zakładkę Sieć/Network, i poszukaj przyczyny');
                }
                return resp.json()
            }).then(data => {
        status_name.innerText = data.choice[status_choice][1];
    })
}

function nameTravel(my_url, name_value, status_name) {
    let token = document.querySelector('#p-token');
    fetch(
        my_url,
        {
            method: 'PATCH', headers: {"X-CSRFToken": token.innerText, 'Content-type': 'application/json'},
            body: JSON.stringify({name: name_value})
        }
    )
        .then(
            function (resp) {
                if (!resp.ok) {
                    alert('Wystąpił błąd! Otwórz devtools i zakładkę Sieć/Network, i poszukaj przyczyny');
                }
                return resp.json()
            }).then(data => {
        status_name.innerText = name_value;
    })
}


document.addEventListener('DOMContentLoaded', function () {
    let stat_selector = document.querySelector('#status');
    let stat_now = document.querySelector('#my-status');
    let name_in = document.querySelector('#trip-name-in');
    let name_now = document.querySelector('#trip-name');
    let editable = [name_now, stat_now].concat(Array.from(document.querySelectorAll('.days')));
    let details = Array.from(document.querySelectorAll('.places'));
    let note = document.querySelector('#note');


    window.addEventListener('click', function (event) {
        stat_selector.classList.add('d-none');
        name_in.classList.add('d-none');
        stat_now.classList.remove('d-none');
        name_now.classList.remove('d-none');
    })


    stat_now.addEventListener('click', function (event) {
        event.stopImmediatePropagation();
        event.preventDefault();
        this.classList.add('d-none');
        stat_selector.classList.remove('d-none');
    })


    editable.forEach(element => {
        element.addEventListener('mouseover', function (event) {
            let span = document.createElement('span');
            span.innerText = 'edytuj';
            span.classList.add('tooltipText');
            this.appendChild(span);
            this.lastElementChild.addEventListener('mouseover', function (event) {
                event.stopImmediatePropagation();
            })
        })
        element.addEventListener('mouseout', function (event) {
            this.lastElementChild.remove();
        });
    })

    details.forEach(element => {
        element.addEventListener('mouseover', function (event) {
            let span = document.createElement('span');
            span.innerText = 'szczegóły';
            span.classList.add('tooltipText');
            span.style = "font-size: 12px";
            this.appendChild(span);
            this.lastElementChild.addEventListener('mouseover', function (event) {
                event.stopImmediatePropagation();
            })
        })
        element.addEventListener('mouseout', function (event) {
            this.lastElementChild.remove();
        });
    })

    note.addEventListener('mouseover', function (event) {
        let span = document.createElement('span');
        span.innerText = 'dodaj';
        span.classList.add('tooltipText');
        this.appendChild(span);
        this.lastElementChild.addEventListener('mouseover', function (event) {
            event.stopImmediatePropagation();
        })
    })
    note.addEventListener('mouseout', function (event) {
        this.lastElementChild.remove();
    });


    stat_selector.addEventListener('click', function (event) {
        event.stopImmediatePropagation()
    })
    stat_selector.addEventListener('change', function (event) {
        this.classList.add('d-none');
        stat_now.classList.remove('d-none');

        const my_url = '/trip/travels/' + stat_selector.dataset.pk;
        const status_choice = stat_selector.value

        statusTravel(my_url, status_choice, stat_now)
    })


    name_now.addEventListener('click', function (event) {
        event.stopImmediatePropagation();
        event.preventDefault();
        this.classList.add('d-none');
        name_in.classList.remove('d-none');
    })

    name_in.addEventListener('click', function (event) {
        event.stopImmediatePropagation()
    })
    name_in.addEventListener('keypress', function (event) {
        if (event.key == 'Enter') {
            this.classList.add('d-none');
            name_now.classList.remove('d-none');

            const my_url = '/trip/travels/' + stat_selector.dataset.pk;
            const name_value = name_in.value
            nameTravel(my_url, name_value, name_now)
        }
    })
})