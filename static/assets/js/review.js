// Select all elements with the "i" tag and store them in a NodeList called "stars"
const stars = document.querySelectorAll(".stars i");
// Loop through the "stars" NodeList
stars.forEach((star, index1) => {
  // Add an event listener that runs a function when the "click" event is triggered
  star.addEventListener("click", () => {
    // Loop through the "stars" NodeList Again
    stars.forEach((star, index2) => {
      // Add the "active" class to the clicked star and any stars with a lower index
      // and remove the "active" class from any stars with a higher index
      index1 >= index2 ? star.classList.add("active") : star.classList.remove("active");
    });

    $('#rating-value').val(star.getAttribute("name"));

  });
});

function deleteReview(id){
    const deleteReviewURL = '/delete-review/'

    // send post request review id
    $.ajax({
        type: "POST",
        url: deleteReviewURL,
        data: {
            csrfmiddlewaretoken: csrfToken,
            action: 'post',
            reviewID: id
        },

        success: function (data){
            if (data.response == true){
                $('#review-' + id).remove()

                // update the current review count when the deletion is successful
                const reviewCount = document.querySelector('#review-count').innerHTML;
                const parseCount = parseInt(reviewCount, 10);

                if (parseCount > 0){
                    $('#review-count').text(parseCount - 1)
                }

            } else if (data.error){
                alert(data.error)
            }
        },

        error: function (errmsg) {},

    })
}