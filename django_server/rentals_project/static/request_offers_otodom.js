const offers_button = document.getElementById("offers_button");
const offers_container = document.getElementById("offers_container");
const spinner = document.getElementById('spinner');
offers_button.addEventListener("click", async () => {
        spinner.classList.add('active'); // Show spinner during fetch
    try {
        const response = await fetch("/get_offers");
        const data = await response.json();
        spinner.classList.remove('active'); // Hide spinner after fetching data
        renderOffers(data.offers)
    } catch (error){
        console.log("ERROR", error);
        spinner.classList.remove('active'); // Hide spinner in case of error

    }
});

function renderOffers(offers) {
        let offersHTML = '<ul class="list-group">';
        offers.forEach(function(offer) {
            offersHTML += '<li class="list-group-item">' +
                '<strong>Title:</strong> ' + offer.title + '<br>' +
                '<strong>Address:</strong> ' + offer.address + '<br>' +
                '<strong>Surface:</strong> ' + offer.surface + '<br>' +
                '<strong>Price (in zł):</strong> ' + offer.price + '<br>' +
                '<strong>Rent:</strong> ' + offer.rent + '<br>' +
                '</li>';
        });
        offersHTML += '</ul>';
        offers_container.innerHTML = offersHTML;
    }