const offersContainer = document.querySelector(".offers-container");
const csrfToken = document.getElementById("csrfToken").value;

async function toggleFavorite(heartIcon) {
    const offerId = heartIcon.closest('.card').id;

    try {
        const response = await fetch("/toggle_favorite", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify(offerId)
        })

        if (response.ok) {
            const offerElement = heartIcon.closest(".card");
            offersContainer.removeChild(offerElement);
        } else {
            console.log("ERROR: ", response.status)
        }
    }  catch (error) {
        console.error('Error:', error);
    }
}

offersContainer.addEventListener('click', function(event) {
    if (event.target.classList.contains('fa-heart')) {
        toggleFavorite(event.target);
    }
});