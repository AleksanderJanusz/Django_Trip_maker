function getCountries() {
    return fetch('/trip/get_countries/')
        .then(
            function (resp) {
                return resp.json()
            })

}

function getPlaces(my_url) {
    return fetch(my_url)
        .then(
            function (resp) {
                return resp.json()
            })

}

function getAttractions(my_url) {
    return fetch(my_url)
        .then(
            function (resp) {
                return resp.json()
            })

}

function displayCountries(response, country) {
    response.forEach(element => {
        let option = document.createElement('option');
        option.value = element.id;
        option.innerText = element.country;
        country.appendChild(option);

    })
}

function displayPlaces(response, place) {
    place.innerHTML = '';
    let first_child = document.createElement('option');
    first_child.innerText = '---------'
    place.appendChild(first_child);
    response.forEach(element => {
        let option = document.createElement('option');
        option.value = element.id;
        option.innerText = element.name;
        place.appendChild(option);
    })
}

function displayAttractions(response, attraction) {
    let selected_id = response.map(element => {
        return Number(element.id)
    })
    for (let child of attraction.children) {
        if (!selected_id.includes(Number(child.value))) {
            child.classList.add('d-none')
        }
    }
}


document.addEventListener('DOMContentLoaded', function () {
    let to_hide = document.querySelector('#id_travel');
    let order = document.querySelector('#id_order');
    let attraction = document.querySelector('#id_place_attraction');
    let country = document.querySelector('#select_country');
    let place = document.querySelector('#select_place');
    let header = document.querySelector('#header');

    for (let child of attraction.children){
        if (child.value == attraction.value){
            const attraction_header = child.innerText
            header.innerText = 'Dzień: ' + order.value + ' ' + attraction_header
        }
    }

    to_hide.parentElement.classList.add('d-none');
    order.previousElementSibling.innerText = 'Dzień numer: ';
    attraction.previousElementSibling.innerText = 'Atrakcja: ';
    attraction.parentElement.classList.add('d-none');

    getCountries().then(function (response) {
        displayCountries(response, country)
    })

    country.addEventListener('change', function (event) {
        attraction.parentElement.classList.add('d-none');
        place.parentElement.classList.remove('d-none');
        let my_url = '/trip/get_place_by_country/?place_country_api=' + this.value;

        getPlaces(my_url).then(function (response) {
            displayPlaces(response, place)
        })
    })

    place.addEventListener('change', function (event) {
        attraction.parentElement.classList.remove('d-none');
        let my_url = '/trip/get_attraction_place/?place_api=' + this.value;

        for(let child of attraction.children){
            child.classList.remove('d-none')
        }

        getAttractions(my_url).then(function (response) {
            displayAttractions(response, attraction)
        })
    })
})