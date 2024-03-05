function calculate_subtotal(){
    const subtotalURL = "/basket/subtotal/";

    $.ajax({
        type: "GET",
        url: subtotalURL,

        success: function(data) {
            $('#subtotal').html(data.subtotal);
            $('#cart-text-quantity').html(data.subtotal);
        },
        error: function() {}
    })
}

function calculate_total_price(id){
    // Calculate its price according to the quantity of the watch
    const getQuantity = parseFloat($('#enter-quantity-' + id).val());
    const getTotalPrice = parseFloat($('#watch-price-' + id).text());
    const resultTotalPrice = getQuantity * getTotalPrice
    $('#total-price-' + id).text(resultTotalPrice);
}

function add_to_cart(id){
    const basketAddURL = "/basket/basket-add/";

    // post request to add the watch to cart
    $.ajax({
        type: "POST",
        url: basketAddURL,
        data: {
            csrfmiddlewaretoken: csrfToken,
            action: 'POST',
            watchID: id,
            watchQty: $('#watch_qty-' + id).val(),
        },

        success: function (response) {
            if (response.success) {
                 $('#add-cart-area').html('<button style="background: green; cursor: default;" class="button" type="button" disabled>Added <i class="bi bi-cart-check-fill"></i></button>')
                 $('#shop-cart-' + id).html('<li class="add_to_cart"><a style="background-color: green; cursor: default; color: white;" onclick="add_to_cart({{watch.id}})" title="added">Added <i class="bi bi-cart-check-fill"></i></a></li>')

                 $('#cart-items').append(`<div id="cart-item-${id}" class="cart_item">
                                               <div class="cart_img">
                                                   <a href="/details/${id}/"><img src="${response.success.image}" alt=""></a>
                                               </div>
                                                <div class="cart_info">
                                                    <a href="/details/${id}/">${response.success.name}</a>

                                                    <span class="quantity">Quantity: ${response.success.quantity}</span>
                                                    <span class="price_cart">$${response.success.total_price}</span>

                                                </div>
                                                <div class="cart_remove">
                                                    <a onclick="delete_from_cart(${id})"><i class="ion-android-close"></i></a>
                                                </div>
                                            </div>`);

                 // Update quantity of watch in cart when add to cart is successful
                 const getCartQuantity = document.querySelector('#cart-quantity').innerHTML;
                 const parseQuantity = parseInt(getCartQuantity, 10);
                 $('#cart-quantity').text(parseQuantity+1);

                 calculate_subtotal();

                 location.reload()
            } else if (response.error) {
                alert(response.error)
            }
        },

        error: function (xhr, errmsg, err) {},
    })
}


function delete_from_cart(id){
    const basketDeleteURL = '/basket/basket-delete/';

    // post request to delete watch from cart
    $.ajax({
        type: "POST",
        url: basketDeleteURL,
        data: {
            csrfmiddlewaretoken: csrfToken,
            action: 'POST',
            watchID: id,
        },

        success: function (response){
            if (response.success){
                $('#cart-item-' + id).remove()

                $('#add-cart-area').html(`<label>quantity</label>
                                    <input id="watch_qty-${id}" onkeydown="return false" min="1" max="${response.success.stock}" value="1" type="number">
                                    <button class="button" onclick="add_to_cart(${id})" type="button">add to cart</button>`);
                $('#shop-cart-' + id).html(`<input id="watch_qty-${id}" min="1" max="100" value="1" type="hidden">
                                                                    <li class="add_to_cart"><a onclick="add_to_cart(${id})" title="add to cart">add to cart</a></li>`);

                // Update quantity of watch in cart when deletion from cart is successful
                const cartQuantity = document.querySelector('#cart-quantity').innerHTML;
                $('#cart-quantity').text(cartQuantity-1);

                $('#product-item-' + id).remove()

                calculate_subtotal();

                location.reload()

            }
        },

        error: function (errmsg) {},
    })
}

