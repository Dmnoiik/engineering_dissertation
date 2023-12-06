const offers_container = document.querySelector(".offers-container");
window.onload = async () => {
    const params = new URLSearchParams(window.location.search);
    const townValue = params.get("town");
    const districtValue = params.get("district");

    const response = await fetch(`get_offers?town=${townValue}&district=${districtValue}`);
    const data = await response.json();
    const website_name = data.website;
    const all_offers = data.offers;
    const overview_par = document.querySelector(".info-overview");
    overview_par.textContent = `${all_offers.length} mieszkań do wynajęcia w ${districtValue}, ${townValue}`;
    for (const offer of all_offers) {
        offers_container.innerHTML += `
    <div class="card">
            <div class="card-image">
                <img src=${offer["image_link"]} alt="offer image link">
            </div>
        <div class="card-info">
            <div class="card-money">
                <p class="card-money-general"><span class="card-money-price">${offer["price"]}</span>/miesięcznie (Czynsz: <span class="card-money-rent">${offer["rent"]}</span>zł)</p>
            </div>
            <div class="card-address">
                <p>${offer["address"]}</p>
            </div>
            <div class="card-details">
                <span class="card-details-info">${offer["rooms"]} ${offer["rooms"] > 1 ? "pokoje" : "pokój"} * ${offer["surface"]}</span>
            </div>
        </div>
        <div class="card-website-info">
            <span class="card-website-name">${website_name}</span>
        </div>
    </div>
        `
    }
}