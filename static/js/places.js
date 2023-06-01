function listOfAttractions(li_main, my_url) {
    fetch(my_url)
        .then(response => response.json())
        .then(data => {
            const ul = document.createElement('ul');
            console.log(data);
            data.forEach(function (element) {
                const li = document.createElement('li');
                const pp = document.createElement('p');
                const p = document.createElement('p');
                const a = document.createElement('a');
                a.href = '/trip/attraction/' + element.id
                a.classList.add('my-links');
                li.classList.add('grand-children');
                pp.innerText = element.name;
                p.innerText = element.description;
                a.appendChild(pp);
                a.appendChild(p);
                li.appendChild(a);
                ul.appendChild(li);
            })
            li_main.appendChild(ul);
            ul.addEventListener("click", function (event) {
                event.stopImmediatePropagation()
            })
        })
}

function apiPlaces(my_url) {
    return fetch(my_url)
        .then(response => response.json())

}

function getCountry() {
    return fetch('/trip/get_countries/')
        .then(response => response.json())
}

function getPlace() {
    return fetch('/trip/get_places/')
        .then(response => response.json())
}

function getAttraction() {
    return fetch('/trip/get_attractions/')
        .then(response => response.json())
}

function attractionToPlace(li) {
    li.addEventListener('click', function (event) {
        const placeId = this.dataset.api;
        if (this.children.length > 0) {
            this.removeChild(this.lastElementChild)

        } else {

            if (this.children.length < 1) {
                for (let element of this.parentElement.children) {
                    if (element.children.length > 0) {
                        element.removeChild(element.firstElementChild);
                    }
                }

                const my_url = '/trip/get_attraction_by_place/?place_api=' + placeId;
                listOfAttractions(li, my_url)
            }
        }
    })
}

function addPlaces(data, country) {

    const ul = document.createElement('ul');
    data.forEach(function (element) {
        const li = document.createElement('li');
        li.innerText = element.name;
        li.dataset.api = element.id;
        li.classList.add('children')
        ul.appendChild(li);


        attractionToPlace(li);


    })
    country.appendChild(ul);
    ul.addEventListener("click", function (event) {
        event.stopImmediatePropagation()
    })
}

function countryPlaceAttractionDisplay(country) {

    country.addEventListener('click', function (event) {
        event.preventDefault()
        const countryId = this.dataset.api

        if (this.children.length > 0) {
            this.removeChild(this.lastElementChild)

        } else {

            if (this.children.length < 1) {
                for (let element of this.parentElement.children) {
                    if (element.children.length > 0) {
                        element.removeChild(element.firstElementChild);
                    }
                }

                const my_url = '/trip/get_place_by_country/?place_country_api=' + countryId
                apiPlaces(my_url).then(data => addPlaces(data, country))
            }
        }
    })

}

function getSpecificCountry(data, search, ul) {
    let my_value = search.value.toLowerCase()
    let countriesList = data.map(data => [data['country'].toLowerCase(), data['id']])

    for (let element of countriesList) {
        if (element[0].includes(my_value)) {
            let li = document.createElement('li');
            li.dataset.api = element[1];
            li.innerText = element[0].charAt(0).toUpperCase() + element[0].slice(1);
            li.classList.add('places');
            countryPlaceAttractionDisplay(li);
            ul.appendChild(li);
        }
    }
}

function getSpecificPlace(data, search, ul) {
    let my_value = search.value.toLowerCase()
    let placesList = data.map(data => [data['name'].toLowerCase(), data['id']])

    for (let element of placesList) {
        if (element[0].includes(my_value)) {
            let li = document.createElement('li');
            li.dataset.api = element[1];
            li.innerText = element[0].charAt(0).toUpperCase() + element[0].slice(1);
            li.classList.add('place-center');

            attractionToPlace(li);
            ul.appendChild(li);
        }
    }
}
function getSpecificAttraction(data, search, ul) {
    let my_value = search.value.toLowerCase()
    let attractionsList = data.map(data => [data['name'].toLowerCase(), data['id'], data['description']])

    for (let element of attractionsList) {
        if (element[0].includes(my_value)) {
            console.log(element[0])
            console.log(my_value)
            let li = document.createElement('li');
            li.dataset.api = element[1];
            li.classList.add('attraction-search');

            let a = document.createElement('a');
            a.href = '/trip/attraction/' + element[1]

            let p1 = document.createElement('p');
            let p2 = document.createElement('p');
            p1.innerText = element[0].toUpperCase();
            p2.innerText = element[2];

            a.appendChild(p1);
            a.appendChild(p2);

            li.appendChild(a);

            ul.appendChild(li);
        }
    }
}

function searchEverything(content, search) {
    let ulCountry = document.createElement('ul');
    ulCountry.classList.add('places');
    content.appendChild(ulCountry);

    let ulPlace = document.createElement('ul');
    ulPlace.classList.add('places');
    content.appendChild(ulPlace);

    let ulAttraction = document.createElement('ul');
    ulAttraction.classList.add('places');
    content.appendChild(ulAttraction);


    search.addEventListener('keyup', function (event) {

        if (event.code === "ShiftLeft" || event.code === "ShiftRight" || event.code === "AltRight" || event.code === "AltLeft") {
            return;
        }
        ulCountry.innerHTML = '';
        ulPlace.innerHTML = '';
        ulAttraction.innerHTML = '';
        if (!this.value) {
            document.querySelector('#country').classList.remove('d-none');
        } else {
            document.querySelector('#country').classList.add('d-none');

            getCountry().then(data => getSpecificCountry(data, this, ulCountry));
            getPlace().then(data => getSpecificPlace(data, this, ulPlace));
            getAttraction().then(data => getSpecificAttraction(data, this, ulAttraction));
        }

    })
}

document.addEventListener('DOMContentLoaded', function () {
    let countries = document.querySelector('#country').children;
    let search = document.querySelector('#search');
    let content = document.querySelector('.content');

    for (let country of countries) {
        countryPlaceAttractionDisplay(country);
    }
    searchEverything(content, search);

})