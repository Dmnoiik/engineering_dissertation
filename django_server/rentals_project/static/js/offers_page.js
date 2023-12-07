const offersContainer = document.querySelector(".offers-container");
const sortElement = document.querySelector(".info-sorting");
const overview_par = document.querySelector(".info-overview");
const sizeInputs = document.querySelectorAll(".size-input");
let websiteName = "";
let allOffers = [];
let filteredOffers = [];

function displayFilteredOrAllOffers() {
    const offersToDisplay = filteredOffers.length ? filteredOffers : allOffers;
    displayOffers(offersToDisplay, websiteName);
}

window.onload = async () => {
    const params = new URLSearchParams(window.location.search);
    const townValue = params.get("town");
    const districtValue = params.get("district");

    const response = await fetch(`get_offers?town=${townValue}&district=${districtValue}`);
    const data = await response.json();
    websiteName = data.website;
    allOffers = data.offers;
    overview_par.textContent = `${allOffers.length} mieszkań do wynajęcia w ${districtValue}, ${townValue}`;
    displayOffers(allOffers, websiteName);
}

function displayOffers(offers, websiteName) {
    offersContainer.innerHTML = ''; // Clear previous content

    for (const offer of offers) {
        const rentPrice = offer.rent !== -1 ? offer.rent : "N/A"
        offersContainer.innerHTML += `
    <div class="card">
    <a href=${offer.link} target="_blank">
            <div class="card-image">
                <img src=${offer["image_link"]} alt="offer image link">
            </div>
        <div class="card-info">
            <div class="card-money">
                <p class="card-money-general"><span class="card-money-price">${offer["price"]}</span>/miesięcznie (Czynsz: <span class="card-money-rent">${rentPrice}</span>)</p>
            </div>
            <div class="card-address">
                <p>${offer["address"]}</p>
            </div>
            <div class="card-details">
                <span class="card-details-info">Pokoje: ${offer["rooms"]} * ${offer["surface"]}m²</span>
            </div>
        </div>
        <div class="card-website-info">
            <span class="card-website-name">${websiteName}</span>
        </div>
        </a>
    </div>
        `;
    }
}

sortElement.addEventListener("change", () => {
    const currentArray = filteredOffers.length ? filteredOffers : allOffers;
    if (sortElement.value === "asc") {
        const sortedOffers = [...currentArray].sort((a, b) => a.price - b.price);
        displayOffers(sortedOffers, websiteName)
    }
    else if (sortElement.value === "desc") {
        const sortedOffers = [...currentArray].sort((a, b) => b.price - a.price);
        displayOffers(sortedOffers, websiteName);
    }
    else if (sortElement.value === "rent-asc") {
        const sortedOffers = [...currentArray].sort((a, b) => a.rent - b.rent);
        displayOffers(sortedOffers, websiteName);
    }
    else if (sortElement.value === "rent-desc") {
        const sortedOffers = [...currentArray].sort((a, b) => b.rent - a.rent);
        displayOffers(sortedOffers, websiteName);
    }
    else {
        displayFilteredOrAllOffers()
    }
})

sizeInputs.forEach(sizeInput => {
    sizeInput.addEventListener("change", (event) => {
        const intValue = parseInt(event.target.value);
        filteredOffers = allOffers.filter(offer => offer.surface >= intValue);
        if (filteredOffers.length === 0) {
            offersContainer.innerHTML = "";
        } else {
        displayFilteredOrAllOffers();
        }
    })
})