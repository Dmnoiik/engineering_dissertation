const townDropdown = document.querySelector(".town-selector");
const districtDropdown = document.querySelector(".district-selector");
const offersButton = document.querySelector(".get-offers-button");
townDropdown.addEventListener("change", async (event) => {
    const cityName = townDropdown.value;
    const response = await fetch(`/get_districts/${cityName}`)
    let districts = await response.json();
    districts = Object.values(districts["districts"]);
    districtDropdown.innerHTML = "";
    districtDropdown.innerHTML += `<option value="" disabled selected>Wybierz dzielnice</option>`
        districts.forEach(district => {
        districtDropdown.innerHTML += `
        <option value="${district}">${district}</option>
        `
    })
    districtDropdown.classList.remove("hidden");
})

districtDropdown.addEventListener("change", async (event) => {
    offersButton.classList.remove("hidden");
})

offersButton.addEventListener("click", async () => {
    const townValue = townDropdown.value;
    const districtValue = districtDropdown.value;
    console.log(townValue);
    window.location = `offers_page?town=${townValue}&district=${districtValue}`;
})
