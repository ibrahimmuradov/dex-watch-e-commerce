function removeCoupon(id){
    removeCouponURL = "/basket/remove-coupon/";

    $.ajax({
        type: "POST",
        url: removeCouponURL,
        data: {
            csrfmiddlewaretoken: csrfToken,
            action: 'post',
            id: id,
        },

        success: function(data){
            location.reload()
        },

        error: function(errmsg){},
    })
}