const csrftoken = getToken('csrftoken')
const add_btns = document.getElementsByClassName('update-cart-btn')
const del_btns = document.getElementsByClassName('cart-delete-item-btn')
let cart = JSON.parse(getCookie('cart'))
let userCookie = getCookie('user')



if(userCookie != 'AnonymousUser'){
    const fields = document.getElementsByClassName('hide')
    for(let i of fields){
        i.style.display = 'none'
    }
}

if(!cart){
    cart = {}
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
}

for(let i of add_btns){
    i.addEventListener('click', async function(e){
        e.preventDefault()
        const productId = this.dataset.product
        const price = this.dataset.price
        const action = this.dataset.action
        const user = this.dataset.user
        const path = window.location.pathname
        if(user === 'AnonymousUser'){
            addCookieItem(productId, price, action, e)
        }else{
            const data = await updateUserOrder(productId, action)
            if(action == 'add' && path != '/cart/'){
                alert('Item Added Successfuly!')
            }
            document.getElementById('total_cart_items_number').textContent = data['total_cart_items'] + data['amount_to_add']
            if(path === '/cart/'){
                const element = e.target
                const qElement = element.parentElement.parentElement.children[0]
                const cartTotlaItemsInfo = document.getElementById('cart-totla-items-info')
                if(action == 'add'){
                    qElement.textContent = Number(qElement.textContent) + 1
                    cartTotlaItemsInfo.innerHTML = `<p>Subtotal (${data['total_cart_items'] + 1} Items): <span style="font-weight: bold;">${data['total_cart_price'].toFixed(2)}</span></p>`
                }else{
                    qElement.textContent = Number(qElement.textContent) - 1
                    cartTotlaItemsInfo.innerHTML = `<p>Subtotal (${data['total_cart_items'] - 1} Items): <span style="font-weight: bold;">${data['total_cart_price'].toFixed(2)}</span></p>`
                    if(qElement.textContent == 0){
                        window.location.reload()
                    }
                }
            }
        }
    })
}

function addCookieItem(productId, price, action, event){
    let path = window.location.pathname

    if(action == 'add'){
        if(cart[productId] == undefined){
            alert('Item Added Successfuly!')
            cart[productId] = {'quantity': 1, 'price': price}
        }else{
            cart[productId]['quantity'] += 1
        }
        document.getElementById('total_cart_items_number').textContent = Number(document.getElementById('total_cart_items_number').textContent) + 1
        if(path == '/cart/'){
            event.target.parentElement.parentElement.children[0].textContent = Number(event.target.parentElement.parentElement.children[0].textContent) + 1
            let totalPrice = 0
            let totalItems = 0
            for(let i in cart){
                totalPrice += Number(cart[i]['quantity']) * Number(cart[i]['price'])
                totalItems += Number(cart[i]['quantity'])
            }
            document.getElementById('cart-totla-items-info').innerHTML = `<p>Subtotal (${totalItems} Items): <span style="font-weight: bold;">${totalPrice.toFixed(2)}</span></p>`
        }
    }

    else if(action == 'remove'){
        cart[productId]['quantity'] -= 1
        if(cart[productId]['quantity'] <= 0){
            delete cart[productId]
            window.location.reload()
        }
        document.getElementById('total_cart_items_number').textContent = Number(document.getElementById('total_cart_items_number').textContent) - 1
        if(path == '/cart/'){
            event.target.parentElement.parentElement.children[0].textContent = Number(event.target.parentElement.parentElement.children[0].textContent) - 1
            let totalPrice = 0
            let totalItems = 0
            for(let i in cart){
                totalPrice += Number(cart[i]['quantity']) * Number(cart[i]['price'])
                totalItems += Number(cart[i]['quantity'])
            }
            document.getElementById('cart-totla-items-info').innerHTML = `<p>Subtotal (${totalItems} Items): <span style="font-weight: bold;">${totalPrice.toFixed(2)}</span></p>`
        }
    }

    else if(action == 'delete'){
        delete cart[productId]
    }

    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
}

for(let i of del_btns){
    i.addEventListener('click', async function(e){
        e.preventDefault()
        const productId = this.dataset.product
        if(userCookie != 'AnonymousUser'){
            console.log(userCookie)
            await deleteOrderItem(productId)
        }else{
            addCookieItem(productId, undefined, 'delete', e)
        }
        window.location.reload()
    })
}

async function deleteOrderItem(productId){
    const url = '/delete_item/'
    const response = await fetch(url + productId + '/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({productId})
    })
    try{
        const data = await response.json()
        return data
    }
    catch{
        return response
    }
}

async function updateUserOrder(productId, action){
    const url = '/update_item/'
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({productId, action})
    })
    try{
        const data = await response.json()
        return data
    }
    catch{
        return response
    }
}

function getToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie != '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getCookie(name){
    const cookieArr = document.cookie.split(';')

    for(let i = 0; i < cookieArr.length; i++){
        let cookiePair = cookieArr[i].split('=')
        if(name == cookiePair[0].trim()){
            return decodeURIComponent(cookiePair[1])
        }
    }
    return false
}
