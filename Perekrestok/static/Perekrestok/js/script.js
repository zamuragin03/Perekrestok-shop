
function Add_to_cart(element) {
    id = element.dataset.id
    counts = $('.item-count')
    data= {
        'id':id,
    }
    // ChangeCart()
    $.ajax({
        type: 'GET',
        url: 'add_to_cart',
        data: data,
        dataType: 'text',
        cache: false,
        success: function (data) {
            if (data == "ok") {
                console.log('pizda_ok')
            }
            else if (data == 'neok') {
                console.log('pizda_neok')
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

