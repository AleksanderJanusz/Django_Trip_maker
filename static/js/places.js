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

function listOfPlaces(country, my_url) {
    fetch(my_url)
        .then(response => response.json())
        .then(data => {
            const ul = document.createElement('ul');
            console.log(data);
            data.forEach(function (element) {
                const li = document.createElement('li');
                li.innerText = element.name;
                li.dataset.api = element.id;
                li.classList.add('children')
                ul.appendChild(li);


                li.addEventListener('click', function (event) {
                    const placeId = this.dataset.api;

                    if (this.children.length < 1) {
                        for (let element of this.parentElement.children) {
                            if (element.children.length > 0) {
                                element.removeChild(element.firstElementChild);
                            }
                        }

                        const my_url = '/trip/get_attraction_by_place/?place_api=' + placeId;
                        console.log(my_url);
                        listOfAttractions(li, my_url)
                    }
                })


            })
            country.appendChild(ul);
            ul.addEventListener("click", function (event) {
                event.stopImmediatePropagation()
            })
        })
}

document.addEventListener('DOMContentLoaded', function () {
    let countries = document.querySelector('#country').children;



    for (let country of countries) {
        country.addEventListener('click', function (event) {
            event.preventDefault()
            const countryId = this.dataset.api

            if (this.children.length < 1) {
                for (let element of this.parentElement.children) {
                    if (element.children.length > 0) {
                        element.removeChild(element.firstElementChild);
                    }
                }

                const my_url = '/trip/get_place_by_country/?place_country_api=' + countryId
                listOfPlaces(country, my_url)
            }
        })
    }


})