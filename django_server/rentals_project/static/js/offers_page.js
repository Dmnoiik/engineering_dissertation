const offersContainer = document.querySelector(".offers-container");
const sortElement = document.querySelector(".info-sorting");
const overview_par = document.querySelector(".info-overview");
const sizeInputs = document.querySelectorAll(".size-input");
// let websiteName = "";
let allOffers = [];
let filteredOffers = [];

function displayFilteredOrAllOffers() {
    const offersToDisplay = filteredOffers.length ? filteredOffers : allOffers;
    displayOffers(offersToDisplay);
}

window.onload = async () => {
    // const params = new URLSearchParams(window.location.search);
    // const townValue = params.get("town");
    // const districtValue = params.get("district");
    //
    // const [otodomResponse, olxResponse] = await Promise.all([
    //     fetch(`get_offers_otodom?town=${townValue}&district=${districtValue}`),
    //     fetch(`get_offers_olx?town=${townValue}&district=${districtValue}`)
    // ])
    // // const response = await fetch(`get_offers_otodom?town=${townValue}&district=${districtValue}`);
    // // const data = await response.json();
    // const otodomData = await otodomResponse.json()
    // const olxData = await olxResponse.json()
    // websiteName = otodomData.website;
    // allOffers = otodomData.offers.concat(olxData.offers);
    // overview_par.textContent = `${allOffers.length} mieszkań do wynajęcia w ${districtValue}, ${townValue}`;
    // displayOffers(allOffers, websiteName);
    // // const responseOlx = await fetch(`get_offers_olx?town=${townValue}&district=${districtValue}`);
    // // const dataOlx = await responseOlx.json();
    const params = new URLSearchParams(window.location.search);
    const townValue = params.get("town");
    const districtValue = params.get("district");

    const otodomPromise = fetch(`get_offers_otodom?town=${townValue}&district=${districtValue}`);

    const olxPromise = fetch(`get_offers_olx?town=${townValue}&district=${districtValue}`);

    const otodomResponse = await otodomPromise;

    const otodomData = await otodomResponse.json();

    allOffers = otodomData.offers;
    overview_par.textContent = `${allOffers.length} mieszkań do wynajęcia w ${districtValue}, ${townValue}`;
    displayOffers(allOffers);

    const olxResponse = await olxPromise;

    const olxData = await olxResponse.json();

    allOffers = allOffers.concat(olxData.offers);
    overview_par.textContent = `${allOffers.length} mieszkań do wynajęcia w ${districtValue}, ${townValue}`;
    displayOffers(allOffers);
}

function displayOffers(offers) {
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
            <span class="card-website-name">${offer.website}</span>
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
        displayOffers(sortedOffers)
    }
    else if (sortElement.value === "desc") {
        const sortedOffers = [...currentArray].sort((a, b) => b.price - a.price);
        displayOffers(sortedOffers);
    }
    else if (sortElement.value === "rent-asc") {
        const sortedOffers = [...currentArray].sort((a, b) => a.rent - b.rent);
        displayOffers(sortedOffers);
    }
    else if (sortElement.value === "rent-desc") {
        const sortedOffers = [...currentArray].sort((a, b) => b.rent - a.rent);
        displayOffers(sortedOffers);
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