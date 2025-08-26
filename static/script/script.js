function load_guests_table() {
    fetch(`${BASE_URL}/load_guests`)
        .then(response => {
            if (response.status === 401) {
                alert("Nie si prihlásený alebo tvoja session vypršala.");
                throw new Error("Unauthorized");
            }

            return response.text()
        })
        .then(html => {
            const container = document.getElementById("personInfo");
            container.innerHTML = html;

            // pridanie tlačidiel do stĺpca Akcia
            const table = container.querySelector("#table_of_guests");


            for (let i = 0; i < table.rows.length; i++) {
                table.rows[i].cells[0].style.display = "none";
            }

            // Pridanie tlačidla do posledného stĺpca
            for (let i = 1; i < table.rows.length; i++) { // začína od 1, preskočí hlavičku
                const guestId = table.rows[i].cells[0].textContent; // ID stále vieme z prvého stĺpca
                const guestChip = table.rows[i].cells[5].textContent;
                const actionCell = table.rows[i].cells[7]; // 8. stĺpec, kde chceme tlačidlo
                const btn = document.createElement("button");
                btn.innerHTML = `<img src="static/icon/bin.svg" width="20" height="20" class="icon">`;
                btn.onclick = () => deleteGuest(guestId, guestChip);
                actionCell.appendChild(btn);

                // Pridáme fade-in animáciu
                table.rows[i].classList.add("fade-in-row");
                table.rows[i].style.animationDelay = `${i * 0.1}s`; // postupné zobrazovanie riadkov
            }
        })
        .catch(error => console.error("Chyba pri načítaní hostí:", error));
}



function reload_guests_table() {
    fetch(`${BASE_URL}/load_guests`)
        .then(response => {
            if (response.status === 401) {
                alert("Nie si prihlásený alebo tvoja session vypršala.");
                throw new Error("Unauthorized");
            }

            return response.text()
        })
        .then(html => {
            const container = document.getElementById("personInfo");
            container.innerHTML = html;

            // pridanie tlačidiel do stĺpca Akcia
            const table = container.querySelector("#table_of_guests");


            for (let i = 0; i < table.rows.length; i++) {
                table.rows[i].cells[0].style.display = "none";
            }

            // Pridanie tlačidla do posledného stĺpca
            for (let i = 1; i < table.rows.length; i++) { // začína od 1, preskočí hlavičku
                const guestId = table.rows[i].cells[0].textContent; // ID stále vieme z prvého stĺpca
                const guestChip = table.rows[i].cells[5].textContent;
                const actionCell = table.rows[i].cells[7]; // 8. stĺpec, kde chceme tlačidlo
                const btn = document.createElement("button");
                btn.innerHTML = `<img src="static/icon/bin.svg" width="20" height="20" class="icon">`;
                btn.onclick = () => deleteGuest(guestId, guestChip);
                actionCell.appendChild(btn);
            }
        })
        .catch(error => console.error("Chyba pri načítaní hostí:", error));
}


function search_guest_button() {
    var search_input = document.getElementById("search_input_guests").value.trim();

    if (!search_input) {
        reload_guests_table();
        return
    }

    fetch(`${BASE_URL}/search_guests?search_input=${encodeURIComponent(search_input)}`, {
        method: 'GET',
        credentials: 'include'
    })
        .then(response => {
            if (response.status === 401) {
                alert("Nie si prihlásený alebo tvoja session vypršala.");
                throw new Error("Unauthorized");
            }
            return response.text();
        })
        .then(html => {
            const container = document.getElementById("personInfo");
            container.innerHTML = html;

            // pridanie tlačidiel do stĺpca Akcia
            const table = container.querySelector("#table_of_guests");


            for (let i = 0; i < table.rows.length; i++) {
                table.rows[i].cells[0].style.display = "none";
            }

            // Pridanie tlačidla do posledného stĺpca
            for (let i = 1; i < table.rows.length; i++) { // začína od 1, preskočí hlavičku
                const guestId = table.rows[i].cells[0].textContent; // ID stále vieme z prvého stĺpca
                const guestChip = table.rows[i].cells[5].textContent;
                const actionCell = table.rows[i].cells[7]; // 8. stĺpec, kde chceme tlačidlo
                const btn = document.createElement("button");
                btn.innerHTML = `<img src="static/icon/bin.svg" width="20" height="20" class="icon">`;
                btn.onclick = () => deleteGuest(guestId, guestChip);
                actionCell.appendChild(btn);
            }
        })
        .catch(console.error)
}

function delete_guest_button() {
    delete_input = prompt("Priložte kartu")

    if (!delete_input) {
        alert("Ste nezadali čip karty")
        return
    }

    if (delete_input.length !== 10) {
        alert("Nesprávna dlžka čisla karty")
        return
    }

    fetch(`${BASE_URL}/delete_guests`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ delete_input })  // Kratšia verzia zápisu (ES6)
    })
        .then(response => {
            if (response.status === 401) {
                alert("Nie si prihlásený alebo tvoja session vypršala.");
                throw new Error("Unauthorized");
            }
            return response.text();
        })
        .then(html => {
            reload_guests_table();
        })
        .catch(console.error)
}

function deleteGuest(delete_id, delete_chip) {
    fetch(`${BASE_URL}/delete_guests_by_id`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ delete_id, delete_chip })
    })
        .then(response => {
            if (response.status === 401) {
                alert("Nie si prihlásený alebo tvoja session vypršala.");
                throw new Error("Unauthorized");
            }
            return response.text();
        })
        .then(html => {
            reload_guests_table();
        })
        .catch(console.error);
}
