

function load_history() {
    fetch(`${BASE_URL}/load_history`)
        .then(response => {
            if (response.status === 401) {
                alert("Nie si prihlásený alebo tvoja session vypršala.");
                throw new Error("Unauthorized");
            }
            return response.text()
        })
        .then(html => {
            const container = document.getElementById("historyInfo");
            container.innerHTML = html;

            // vyberieme tabuľku v histórii (predpokladám, že má id="table_of_history")
            const table = container.querySelector("#table_of_history");
            if (!table) return;

            // pridáme fade-in pre každý riadok
            for (let i = 1; i < table.rows.length; i++) { // preskočíme hlavičku
                table.rows[i].classList.add("fade-in-row");
                table.rows[i].style.animationDelay = `${i * 0.1}s`; // postupné zobrazovanie
            }
        })
        .catch(error => {
            console.error("Chyba pri načítaní histórie:", error);
        });
}


function searchHistory() {

    var name = document.getElementById("search_name_id").value.trim();

    if (!name) {
        load_history()
        return
    }

    fetch(`${BASE_URL}/search_on_history`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ name })  // Kratšia verzia zápisu (ES6)
    })
        .then(response => {
            if (response.status === 401) {
                alert("Nie si prihlásený alebo tvoja session vypršala.");
                throw new Error("Unauthorized");
            }
            return response.text();
        })
        .then(html => {
            const container = document.getElementById("historyInfo");
            container.innerHTML = html;
        })
        .catch(console.error);
}

function search_key_history() {

    var search_key_id = document.getElementById("search_key_id").value.trim();

    if (!search_key_id) {
        load_history_keys()
        return
    }

    fetch(`${BASE_URL}/search_employee_on_history`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ search_key_id })  // Kratšia verzia zápisu (ES6)
    })
        .then(response => {
            if (response.status === 401) {
                alert("Nie si prihlásený alebo tvoja session vypršala.");
                throw new Error("Unauthorized");
            }
            return response.text();
        })
        .then(html => {
            const container = document.getElementById("historyInfo");
            container.innerHTML = html;
        })
        .catch(console.error);
}