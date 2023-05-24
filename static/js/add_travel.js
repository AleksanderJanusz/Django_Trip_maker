function listOfAttractions(li_main, my_url, div_form, my_select) {
    fetch(my_url)
        .then(response => response.json())
        .then(data => {
            div_form.firstElementChild.classList.remove('d-none')
            const data_ids = data.map(function (element) {
                return element.id;
            })

            for (let option of my_select.children) {
                if (!data_ids.includes(Number(option.value))) {
                    option.classList.add('d-none');
                }
            }
            my_select.firstElementChild.classList.remove('d-none');

        })
}

function listOfPlaces(my_url, div_place, div_form) {
    fetch(my_url)
        .then(response => response.json())
        .then(data => {
            const label = document.createElement('label');
            const select = document.createElement('select');
            select.name = 'place';
            select.id = 'select_place';
            label.innerText = 'Wybierz Miejsce';
            label.htmlFor = select.id;

            const option = document.createElement('option');
            option.innerText = '---------';
            select.appendChild(option);

            data.forEach(function (element) {
                const option = document.createElement('option');
                option.value = element.id;
                option.innerText = element.name;
                select.appendChild(option);
            })

            div_place.appendChild(label);
            div_place.appendChild(select);

            select.addEventListener('change', function (event) {
                let placeId = this.value;
                const my_url = '/trip/get_attraction_place/?place_api=' + placeId;
                let my_select = div_form.firstElementChild.lastElementChild;

                for(let option of my_select.children){
                    option.classList.remove('d-none')
                }

                div_form.firstElementChild.lastElementChild.selectedIndex = 0;
                listOfAttractions(select, my_url, div_form, my_select)
            })

        })
}

document.addEventListener('DOMContentLoaded', function () {
    let div_form = document.querySelector('#day_form')
    let select_country = document.querySelector('#select_country')
    let div_place = document.querySelector('#div_place')

    console.log(window.url)
    div_form.firstElementChild.classList.add('d-none')

    select_country.addEventListener('change', function (event) {
        div_form.firstElementChild.classList.add('d-none')
        let countryId = this.value;
        div_place.innerHTML = '';
        const my_url = '/trip/get_place_by_country/?place_country_api=' + countryId;
        div_form.firstElementChild.lastElementChild.selectedIndex = 0;
        listOfPlaces(my_url, div_place, div_form)
    })

})