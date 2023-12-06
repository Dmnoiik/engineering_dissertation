const offers_button = document.getElementById("get-offers-button");
const offers_container = document.getElementById("offers_container");
offers_button.addEventListener("click", async () => {
    const selected_district = document.querySelector(".district-tile.selected");
    offers_button.disabled = true;
    const town = document.querySelector(".city-tile.selected h5")
        try {
            const response = await fetch(`/get_offers?district=${selected_district.textContent}&town=${town.textContent}`);
            const data = await response.json();
            offers_button.disabled = false;
            renderOffers(data.offers)
        } catch (error){
            console.log("ERROR", error);
        }
});

function renderOffers(offers) {
let offersHTML = '<div class="row">';
offers.forEach(function(offer) {
    offersHTML +=
        `<div class="col-sm-6 col-md-4 col-lg-3">
            <div class="card mb-3">
                <div class="card-body">
                    <h5 class="card-title">${offer.title}</h5> 
                    <p class="card-text">
                        <strong>Address:</strong> ${offer.address} <br>
                        <strong>Surface:</strong> ${offer.surface} <br>
                        <strong>Price (in zł):</strong> ${offer.price} <br>
                        <strong>Rent:</strong> ${offer.rent}
                    </p>
                </div>
            </div>
        </div>`;
});
offersHTML += '</div>';
offers_container.innerHTML = offersHTML;
    }