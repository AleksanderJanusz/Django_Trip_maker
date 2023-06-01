document.addEventListener('DOMContentLoaded', function (){
    let menu = document.querySelector('#menu');
    let leftMenu = document.querySelector('#left-menu');
    let add_button = document.querySelector('#add_button');
    let trip_button = document.querySelector('#trip');

    menu.addEventListener('click', function(event){
        event.preventDefault();
        event.stopImmediatePropagation();
        leftMenu.classList.toggle('d-none');
        leftMenu.addEventListener('click', function (event){
            event.stopImmediatePropagation()
        })
    })

    add_button.addEventListener('click', function (event){
        event.preventDefault();
        event.stopImmediatePropagation();
        add_button.nextElementSibling.classList.toggle('d-none');
    })

    trip_button.addEventListener('click', function (event){
        event.preventDefault();
        event.stopImmediatePropagation();
        this.nextElementSibling.classList.toggle('d-none');
    })

    window.addEventListener('click', function (event){
        if (!leftMenu.classList.contains('d-none')){
            leftMenu.classList.add('d-none')
        }
        if (!add_button.classList.contains('d-none')){
            add_button.nextElementSibling.classList.add('d-none')
        }
    })


})