document.addEventListener('DOMContentLoaded', function (){
    let menu = document.querySelector('#menu');
    let leftMenu = document.querySelector('#left-menu');

    menu.addEventListener('click', function(event){
        event.preventDefault();
        event.stopImmediatePropagation()
        leftMenu.classList.toggle('d-none');
    })
    window.addEventListener('click', function (event){
        if (!leftMenu.classList.contains('d-none')){
            leftMenu.classList.add('d-none')
        }

    })
})