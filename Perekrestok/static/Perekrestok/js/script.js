
function Add_to_cart(element) {
    id = element.dataset.id
    count_tags = $('.count-tag')

    i = element.dataset.counter - 1
    new_count =parseInt(count_tags[i].dataset.count) + 1
    count_tags[i].dataset.count = new_count
    count_tags[i].innerHTML = new_count
    $.ajax({
        type: 'GET',
        url: 'add_to_cart',
        data: { 'id': id, },
        dataType: 'text',
        cache: false,
        success: function (data) {
            if (data == "ok") {
                console.log('ok')
            }
            else if (data == 'neok') {

            }
        }
    })
}

function ChangeCart() {
    sum = 0

    count_labels = document.getElementsByClassName('item-count')
    for (var i = 0; i < count_labels.length; i++) {
        sum += parseInt((count_labels[i]).dataset.count)
    }
    cart = document.getElementById('cart')
    cart.innerHTML = `Корзина(${sum})`
}

function ShowCart() {
    var element = document.getElementById("cart-items");
    element.classList.remove("hidden");
}
function Invise() {
    var element = document.getElementById("cart-items");
    element.classList.add("hidden");
}

function GetCategory(button) {
    // var element = document.getElementById("cart-items");
    // button.dataset.name
    // var element = document.getElementById("current-cat");
    // element.dataset.name=button.dataset.name
    console.log(button.name)
}

function DeleteItem(el) {
    console.log(el.dataset.id)
    id = el.dataset.id
    counter = el.dataset.counter - 1
    console.log(counter)

    $.ajax({
        type: 'GET',
        url: 'delete_from_cart',
        data: { 'id': el.dataset.id },
        dataType: 'text',
        cache: false,
        success: function (data) {
            if (data == "ok") {
                a = document.getElementsByClassName('cart-flex-wrapper')
                console.log(a[counter])
                location.reload()
                // a[counter].remove()
            }
            else if (data == 'neok') {
            }
        }
    })
}

function change_item_count(el, flag) {
    console.log(el.dataset.id)
    id = el.dataset.id
    counter = el.dataset.counter - 1
    console.log(counter)
    $.ajax({
        type: 'GET',
        url: 'change_cart_amount',
        data: {
            'id': el.dataset.id,
            'flag': flag
        },
        dataType: 'text',
        cache: false,
        success: function (data) {
            if (data == "ok") {
                // a = document.getElementsByClassName('cart-flex-wrapper')
                // console.log(a[counter])
                location.reload()
                // a[counter].remove()
            }
            else if (data == 'neok') {
                console.log('neok')
            }
        }
    })
}

