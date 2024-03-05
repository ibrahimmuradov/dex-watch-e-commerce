
function wishlist(id) {
    const wishlistURL = "/wishlist/";

    // post request to add the watch to wishlist
    $.ajax({
        type: "POST",
        url: wishlistURL,
        data: {
            csrfmiddlewaretoken: csrfToken,
            action: 'post',
            watchID: id,
        },

        success: function (data){
            if (data.response == true){
                // Update wishlist when watch is successfully added to user wishlist
                $('#wishlist-icon-' + id).css('color', 'red');
                $('#wishlist-text-' + id).html(`<i id="wishlist-icon-${id}" style="color: red" class="icon-heart"></i> Added`);
            } else if (data.response == false) {
                $('#wishlist-icon-' + id).css('color', 'gray');
                $('#wishRow-' + id).remove();
                $('#wishlist-text-' + id).html(`<i id="wishlist-icon-${id}" class="icon-heart"></i> Add to Wishlist`);
            } else if (data.error){
                alert(data.error)
            }
        },

        error: function(errmsg){},
    });

}