const mainImg = document.getElementById('single-product-main-img')
const subs = document.querySelectorAll('.sub-img img')

subs.forEach(x => x.addEventListener('click', changeImg))

function changeImg(){
    mainImg.src = this.src
}
