const offersContainer = document.querySelector(".offers-container");
const sortElement = document.querySelector(".info-sorting");
const overview_par = document.querySelector(".info-overview");
const sizeInputs = document.querySelectorAll(".size-input");
const authenticationEl = document.querySelector(".authentication");
const isAuthenticated = authenticationEl.getAttribute("data-authenticated") === "True";
const csrfToken = document.getElementById("csrfToken").value;
const loadingEl = document.querySelector(".loading-container");
const loadingParEl = document.querySelector(".loading-paragraph");
const minPriceInputEl = document.querySelector(".price-min-input")
const maxPriceInputEl = document.querySelector(".price-max-input")
const filterBtn = document.querySelector(".filter-btn");
const reverseFilterBtn = document.querySelector(".reverse-filter-btn");
let allOffers = [];
let filteredOffers = [];

function displayFilteredOrAllOffers() {
    // Check if any filter has been applied
    const isAnyFilterApplied =
        minPriceInputEl.value !== "" ||
        maxPriceInputEl.value !== "" ||
        document.querySelector("input[name='size-input']:checked") !== null ||
        document.querySelectorAll(".rooms-input:checked").length > 0;

    // Determine which set of offers to display
    const offersToDisplay = isAnyFilterApplied ? filteredOffers : allOffers;

    displayOffers(offersToDisplay);
}

async function getFavoriteOffers() {
    if (isAuthenticated) {
        const response = await fetch("/get_favorite_offers")
        const data = await response.json();
        const favoriteOffersData = data["favorite_offers"];
        favoriteOffersData.forEach(offer => {
            const offerId = offer["offer_id"];
            const availableOffer = document.getElementById(`${offerId}`);
            if (availableOffer) {
                const heartIcon = availableOffer.querySelector(".fa-heart");
                heartIcon.classList.add("is-favorite");
            }
        })
    }
}
window.onload = async () => {
    try {
        loadingEl.style.display = "flex";
        const params = new URLSearchParams(window.location.search);
        const townValue = params.get("town");
        const districtValue = params.get("district");
        overview_par.textContent = `Ładowanie ofert mieszkań w ${districtValue}, ${townValue}`;

        const otodomPromise = fetch(`get_offers_otodom?town=${townValue}&district=${districtValue}`);
        const olxPromise = fetch(`get_offers_olx?town=${townValue}&district=${districtValue}`);

        const processResponse = async (responsePromise, source) => {
            const response = await responsePromise;
            if (response.ok) {
                const data = await response.json();
                allOffers = allOffers.concat(data.offers);
                overview_par.textContent = `${allOffers.length} mieszkań do wynajęcia w ${districtValue}, ${townValue}`;
                displayOffers(allOffers);
            } else {
                console.error(`Failed to fetch offers from ${source}`);
            }
        };

        // Handle each promise separately
        processResponse(otodomPromise, 'Otodom').finally(() => {
            loadingEl.style.display = "none";
        });

        processResponse(olxPromise, 'OLX').finally(() => {
            loadingEl.style.display = "none";
        });

        await getFavoriteOffers();
    } catch (error) {
        console.error("An error occurred:", error);
        loadingEl.style.display = "none";
    }
};


function displayOffers(offers) {
    offersContainer.innerHTML = '';
    if (offers.length === 0) {
        offersContainer.innerHTML = `
        <div class="no-offers-container">
        <img src="/static/images/smutny_domek2.svg" class="no-offers-image">
        <p class='no-offers-alert'>Nie udało się znaleźć lub dopasować żadnych ofert. Może warto zresetować filtry lub znaleźć inną dzielnicę?</p>
        </div>`
    }
    for (const offer of offers) {
        const rentPrice = offer.rent !== -1 ? offer.rent : "N/A"
        let heartIconHtml = '';

        if (isAuthenticated) {
            heartIconHtml = `
                    <div class="heart-icon">
                <i class="fas fa-heart"></i>
            </div>`
        }


        offersContainer.innerHTML += `
    <div class="card" id="${offer["offer_id"]}">
    ${heartIconHtml}
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
                <span class="card-details-info">Pokoje: ${offer["rooms"]} • ${offer["surface"]}m²</span>
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
    } else if (sortElement.value === "desc") {
        const sortedOffers = [...currentArray].sort((a, b) => b.price - a.price);
        displayOffers(sortedOffers);
    } else if (sortElement.value === "rent-asc") {
        const sortedOffers = [...currentArray].sort((a, b) => a.rent - b.rent);
        displayOffers(sortedOffers);
    } else if (sortElement.value === "rent-desc") {
        const sortedOffers = [...currentArray].sort((a, b) => b.rent - a.rent);
        displayOffers(sortedOffers);
    } else {
        displayFilteredOrAllOffers()
    }
})

async function toggleFavorite(heartIcon) {
    heartIcon.classList.toggle('is-favorite');
    const offerId = heartIcon.closest('.card').id; // Assuming offer_id is the HTML element ID
    const offer = allOffers.find(offer => offer["offer_id"] === offerId)

    try {
        const response = await fetch("/toggle_favorite", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify(offer)
        })
    } catch (error) {
        console.error('Error:', error);
    }
}

offersContainer.addEventListener('click', function (event) {
    if (event.target.classList.contains('fa-heart')) {
        toggleFavorite(event.target);
    }
});

filterBtn.addEventListener("click", () => {
    const minPrice = parseFloat(minPriceInputEl.value) || null;
    const maxPrice = parseFloat(maxPriceInputEl.value) || null;
    let checkedRadioInput = document.querySelector("input[name='size-input']:checked");
    checkedRadioInput = checkedRadioInput ? parseInt(checkedRadioInput.value) : null;

    const selectedRoomsCheckboxes = document.querySelectorAll(".rooms-input:checked");
    const selectedRooms = Array.from(selectedRoomsCheckboxes).map(checkbox => parseInt(checkbox.value));

    filteredOffers = allOffers.filter(offer => {
        // Price filter
        const priceFilter = (minPrice === null || offer.price >= minPrice) &&
            (maxPrice === null || offer.price <= maxPrice);

        // Size filter
        const sizeFilter = checkedRadioInput === null || offer.surface >= checkedRadioInput;

        // Rooms filter
        const roomsFilter = selectedRooms.length === 0 || selectedRooms.includes(offer.rooms);

        return priceFilter && sizeFilter && roomsFilter;
    });

    displayFilteredOrAllOffers();
});

reverseFilterBtn.addEventListener("click", () => {
    minPriceInputEl.value = "";
    maxPriceInputEl.value = "";
    const checkedSizeInput = document.querySelector("input[name='size-input']:checked");
    if (checkedSizeInput) {
        checkedSizeInput.checked = null;
    }
    const selectedRoomsCheckboxes = document.querySelectorAll(".rooms-input:checked");
    if (selectedRoomsCheckboxes) {
        selectedRoomsCheckboxes.forEach(checkbox => {
            checkbox.checked = null;
        })
    }

    displayOffers(allOffers);
})





