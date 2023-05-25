function statusTravel(my_url, status_choice, status_name) {
    let token = document.querySelector('#p-token');
    fetch(
        my_url,
        {method: 'PATCH', headers: {"X-CSRFToken": token.innerText, 'Content-type': 'application/json'},
        body: JSON.stringify({status: status_choice})}
    )
        .then(
            function (resp) {
                if (!resp.ok) {
                    alert('Wystąpił błąd! Otwórz devtools i zakładkę Sieć/Network, i poszukaj przyczyny');
                }
                return resp.json()
            }).then(data => {
                 status_name.innerText = 'Status: ' + data.choice[status_choice][1];
    })
}

document.addEventListener('DOMContentLoaded', function () {
    let travel = document.querySelectorAll('.button-list');
    let status = document.querySelectorAll('.button-list-status');

    window.addEventListener('click', function () {
        status.forEach(status_element => {
            status_element.classList.add('d-none');
            status_element.nextElementSibling.lastElementChild.firstElementChild.classList.add('d-none');
        })
    })

    travel.forEach(element => element.addEventListener('mouseover', function () {

        status.forEach(status_element => {
            status_element.classList.add('d-none');
            status_element.nextElementSibling.lastElementChild.firstElementChild.classList.add('d-none');
        })
        element.nextElementSibling.classList.remove('d-none');

    }))

    status.forEach(element => element.addEventListener('click', function (event) {
        event.stopImmediatePropagation();
        event.preventDefault();
        let my_ul = element.nextElementSibling.lastElementChild.firstElementChild;
        my_ul.classList.remove('d-none');

        my_ul.addEventListener('mouseout', function (){
            this.classList.add('d-none');
        })

        for (let pick_status of my_ul.children) {
            pick_status.addEventListener('mouseover', function (event){
                event.stopImmediatePropagation();
                this.parentElement.classList.remove('d-none');
            })
            pick_status.addEventListener('click', function (event) {
                event.stopImmediatePropagation();
                this.parentElement.classList.add('d-none');

                const my_url = '/trip/travels/' + element.id;
                const status_choice = this.id;
                const status_name = this.parentElement.parentElement.parentElement.parentElement.firstElementChild.nextElementSibling

                statusTravel(my_url, status_choice, status_name)
            })
        }
    }))
})
