const cityTiles = document.querySelectorAll(".city-tile");
const districtsContainer = document.getElementById("districts");
const getOffersButton = document.getElementById("get-offers-button")
cityTiles.forEach(function(tile) {
    tile.addEventListener("click", async function() {
        const cityName = tile.id;
        cityTiles.forEach(city => {
            city.classList.remove("selected");
        });

        tile.classList.add("selected");
        getOffersButton.classList.add("hidden");
        const response = await fetch(`/get_districts/${cityName}`)
        let data = await response.json();
        data = Object.values(data["districts"]);

        districtsContainer.innerHTML = ""; // Clear previous content
            data.forEach(district => {
                const districtTile = document.createElement("div");
                districtTile.classList.add("district-tile");
                districtTile.innerText = district;
                districtsContainer.appendChild(districtTile);

                // Click event to toggle selected class
                districtTile.addEventListener("click", function(event) {
                    const selectedDistrict = event.target;
                    const allDistricts = document.querySelectorAll(".district-tile");
                    allDistricts.forEach(district => district.classList.remove("selected"));
                    selectedDistrict.classList.add("selected");
                    getOffersButton.classList.remove("hidden");

                });
            });

            districtsContainer.style.display = "flex";
    });
});
