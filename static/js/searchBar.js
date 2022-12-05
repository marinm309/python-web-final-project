const search_field = document.getElementById('search-field');

document.addEventListener('click', function(event) {
    let isClickInsideElement = search_field.contains(event.target)
    let search = document.getElementById('search-form')
    if (!isClickInsideElement) {
        search.style.outline = 'none'
    }else{
        search.style.outline = '3px solid #ffa500'
    };
});