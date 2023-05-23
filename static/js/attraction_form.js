document.addEventListener('DOMContentLoaded', function (){
    let checkbox = document.querySelector('#my_checkbox');
    let from = document.querySelector('#from');
    let to = document.querySelector('#to');
    checkbox.addEventListener('change', function (event){
        from.classList.toggle('d-none')
        to.classList.toggle('d-none')
    })
})