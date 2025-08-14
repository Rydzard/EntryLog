function load_guests_table() {
    fetch('https://localhost:5000/api/load_guests')
        .then(response => response.text())
        .then(html => {
            const container = document.getElementById("personInfo");
            container.innerHTML = html;

            // pridanie tlačidiel do stĺpca Akcia
            const table = container.querySelector("#table_of_guests");
            for (let i = 1; i < table.rows.length; i++) { // začína od 1, aby sme preskočili hlavičku
                const cip = table.rows[i].cells[5].textContent; // predpokladáme, že cip je 6. stĺpec (index 5)
                const actionCell = table.rows[i].cells[7];      // Akcia je 8. stĺpec (index 7)
                const btn = document.createElement("button");
                btn.textContent = "Odstrániť";
                btn.onclick = () => deleteGuest(cip);
                actionCell.appendChild(btn);
            }
        })
        .catch(error => console.error("Chyba pri načítaní hostí:", error));
}


function search_guest_button() {
    var search_input = document.getElementById("search_input_guests").value.trim();

    if (!search_input) {
        load_guests_table()
        return
    }

    fetch(`https://localhost:5000/api/search_guests?search_input=${encodeURIComponent(search_input)}`, {
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
            document.getElementById("personInfo").innerHTML = html;
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

    fetch('https://localhost:5000/api/delete_guests', {
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
        document.getElementById("personInfo").innerHTML = html;
    })
    .catch(console.error)

    load_guests_table();
}

function deleteGuest(delete_input) {
    fetch('https://localhost:5000/api/delete_guests', {
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
        document.getElementById("personInfo").innerHTML = html;
    })
    .catch(console.error)

    load_guests_table();
}