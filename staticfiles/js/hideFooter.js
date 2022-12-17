const elements = document.getElementsByTagName('input')
const footer = document.getElementsByTagName('footer')[0]

for(let i of elements){
    i.addEventListener('focus', hideFooter)
    i.addEventListener('blur', showFooter)
}

function hideFooter(){
    footer.style.display = 'none'
}

function showFooter(){
    footer.style.display = 'block'
}