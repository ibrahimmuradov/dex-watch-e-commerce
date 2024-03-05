 $(document).ready(function(){

    const total_watch = JSON.parse(document.getElementById('total_watch').textContent);

    var currentUrl = window.location.href;

    // Create a URL object
    var url = new URL(currentUrl);

    // Get the search parameters (query string)
    var searchParams = url.searchParams;

    // Extract the filter query part from the search parameters
    var filterQuery = searchParams.toString();

    $('#load_more').attr('href', `?${filterQuery}&load_more=${total_watch}`);

    var selectElement = document.getElementById("short");

    // Add event listener to listen for changes in selection
    selectElement.addEventListener("change", function() {
        // Get the selected option
        var selectedOption = selectElement.options[selectElement.selectedIndex];

        // Get the value of the selected option
        var selectedValue = selectedOption.value;

        if (searchParams.has('sort_by')) {
            searchParams.set('sort_by', selectedValue)

            url.search = searchParams.toString();

            update_url = url.toString();

        } else {
            // Log or use the selected value
            update_url = `?${filterQuery}&sort_by=${selectedValue}`;
        }

        window.location.href = update_url;

    });


    // Retrieve the query parameters from the URL
    var urlParams = new URLSearchParams(window.location.search);

    var filterDict = {
        'category': urlParams.getAll('categoryFilter'),
        'dial-color': urlParams.getAll('dial_color'),
        'band-color': urlParams.getAll('band_color'),
        'style': urlParams.getAll('styleFilter'),
        'functionality': urlParams.getAll('functionalityFilter'),
        'material': urlParams.getAll('materialFilter'),
        'movement': urlParams.getAll('movementFilter'),
        'material': urlParams.getAll('materialFilter'),
        'gender': urlParams.getAll('genderFilter'),
        'min-price': urlParams.getAll('min-price'),
        'max-price': urlParams.getAll('max-price'),
    };

    for(var val in filterDict) {
        for (var id in filterDict[val]){
            $('#' + val + '-' + filterDict[val][id].toLowerCase().replace(/\s+/g, '-')).prop('checked', true);
            // It finds and checked the selected filter element according to the data in the url
            // With lowercase and replace, it corrects the spaces and letters of the data to find the input element equal to the data in the url.
        }
    }

    // Filtering by price
    if (filterDict['max-price'].length > 0){
        const rangeInput = document.querySelectorAll(".range-input input");
        const range = document.querySelector(".slider .progress");
        const priceInput = document.querySelectorAll(".price-input input");

        const minPrice = filterDict['min-price'];
        const maxPrice = filterDict['max-price'];

        $('#min-price').val(minPrice);
        $('#max-price').val(maxPrice);

        $('#min-range').val(minPrice);
        $('#max-range').val(maxPrice);

        range.style.left = (minPrice / rangeInput[0].max) * 100 + "%";
        range.style.right = 100 - (maxPrice / rangeInput[1].max) * 100 + "%";
    }

  });