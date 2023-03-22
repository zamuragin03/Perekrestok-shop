
function CreateOrder(element) {
    id = element.dataset.id
    count_tags = $('.count-tag')

    i = element.dataset.counter - 1
    new_count = parseInt(count_tags[i].dataset.count) + 1
    count_tags[i].dataset.count = new_count
    count_tags[i].innerHTML = new_count
    $.ajax({
        type: 'GET',
        url: 'create_order',
        data: {},
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




function Add_to_cart(element) {
    id = element.dataset.id
    count_tags = $('.count-tag')

    i = element.dataset.counter - 1
    new_count = parseInt(count_tags[i].dataset.count) + 1
    count_tags[i].dataset.count = new_count
    count_tags[i].innerHTML = new_count
    $.ajax({
        type: 'GET',
        url: 'add_to_cart',
        data: { 'id': id, '_token': $('meta[name="csrf-token"]').attr('content') },
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
                // a = document.getElementsByClassName('cart-flex-wrapper')
                // console.log(a[counter])
                location.reload() 
                // a[counter].remove() //dele
            }
            else if (data == 'neok') {
            }
        }
    })
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
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
            'flag': flag,
        },
        // headers: {
        //     "X-Requested-With": "XMLHttpRequest",
        //     "X-CSRFToken": getCookie("csrftoken"),  // don't forget to include the 'getCookie' function
        //   },
        dataType: 'text',
        cache: false,
        success: function (data) {
            if (data == "ok") {
                console.log('ok')
                // a = document.getElementsByClassName('cart-flex-wrapper')
                // console.log(a[counter])
                location.reload() //uncomment
                // a[counter].remove() //dele
            }
            else if (data == 'neok') {
                console.log('neok')
            }
        }
    })
}

function AddToCartFromShowPage(element){
    id = element.dataset.id
    count_tag = $('.item-count')  
    new_count = parseInt(count_tag[0].dataset.count) + 1
    count_tag[0].dataset.count = new_count
    count_tag[0].innerHTML = new_count  + ' шт'
    $.ajax({
        type: 'GET',
        url: '/add_to_cart/',
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
