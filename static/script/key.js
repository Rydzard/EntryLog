
function load_keys_database() {
    fetch(`${BASE_URL}/load_keys_database`)
        .then(response => response.text())
        .then(html => {
            const container = document.getElementById("historyInfo");
            container.innerHTML = html;

            // pridanie tlačidiel do stĺpca Akcia
            const table = container.querySelector("#table_of_guests");
            // Pridanie tlačidla do posledného stĺpca
            for (let i = 1; i < table.rows.length; i++) { // začína od 1, preskočí hlavičku
                const employeeName = table.rows[i].cells[1].textContent; // ID stále vieme z prvého stĺpca
                const employeeKey = table.rows[i].cells[0].textContent;
                const deleteColumns = table.rows[i].cells[5];
                const btn = document.createElement("button");
                btn.innerHTML = `<img src="static/icon/bin.svg" width="20" height="20" class="icon">`;
                btn.onclick = () => deleteKey(employeeName, employeeKey);
                deleteColumns.appendChild(btn);

                // Pridáme fade-in animáciu
                table.rows[i].classList.add("fade-in-row");
                table.rows[i].style.animationDelay = `${i * 0.1}s`; // postupné zobrazovanie riadkov
            }
        })
        .catch(error => {
            console.error("Chyba pri načítaní hostí:", error);
        });
}


function reload_keys_database() {
    fetch(`${BASE_URL}/load_keys_database`)
        .then(response => response.text())
        .then(html => {
            const container = document.getElementById("historyInfo");
            container.innerHTML = html;

            // pridanie tlačidiel do stĺpca Akcia
            const table = container.querySelector("#table_of_guests");
            // Pridanie tlačidla do posledného stĺpca
            for (let i = 1; i < table.rows.length; i++) { // začína od 1, preskočí hlavičku
                const employeeName = table.rows[i].cells[1].textContent; // ID stále vieme z prvého stĺpca
                const employeeKey = table.rows[i].cells[0].textContent;
                const deleteColumns = table.rows[i].cells[5];
                const btn = document.createElement("button");
                btn.innerHTML = `<img src="static/icon/bin.svg" width="20" height="20" class="icon">`;
                btn.onclick = () => deleteKey(employeeName, employeeKey);
                deleteColumns.appendChild(btn);
            }
        })
        .catch(error => {
            console.error("Chyba pri načítaní hostí:", error);
        });
}

function search_key() {
    var key_number = document.getElementById("search_key_id").value;

    if (!key_number) {
        reload_keys_database();
        return
    }

    if (key_number <= 0) {
        alert("Zadejte číslo klíče")
        return
    }

    fetch(`${BASE_URL}/search_key?key_number=${encodeURIComponent(key_number)}`, {
        method: 'GET',
        credentials: 'include'
    })
        .then(response => response.text())
        .then(html => {
            const container = document.getElementById("historyInfo");
            container.innerHTML = html;

            // pridanie tlačidiel do stĺpca Akcia
            const table = container.querySelector("#table_of_guests");
            // Pridanie tlačidla do posledného stĺpca
            for (let i = 1; i < table.rows.length; i++) { // začína od 1, preskočí hlavičku
                const employeeName = table.rows[i].cells[1].textContent; // ID stále vieme z prvého stĺpca
                const employeeKey = table.rows[i].cells[0].textContent;
                const deleteColumns = table.rows[i].cells[5];
                const btn = document.createElement("button");
                btn.innerHTML = `<img src="static/icon/bin.svg" width="20" height="20" class="icon">`;
                btn.onclick = () => deleteKey(employeeName, employeeKey);
                deleteColumns.appendChild(btn);
            }
        })
        .catch(console.error)
}

function load_history_keys() {

    fetch(`${BASE_URL}/load_history_keys`)
        .then(response => response.text())
        .then(html => {
            const container = document.getElementById("historyInfo");
            container.innerHTML = html;

            // vyberieme tabuľku
            const table = container.querySelector("#table_of_history");
            if (!table) return;

            // pridáme fade-in pre každý riadok, preskočíme hlavičku
            for (let i = 1; i < table.rows.length; i++) {
                table.rows[i].classList.add("fade-in-row");
                table.rows[i].style.animationDelay = `${i * 0.1}s`;
            }
        })
        .catch(error => {
            console.error("Chyba pri načítaní hostí:", error);
        });
}

function deleteKey(employeeName, employeeKey) {
    fetch(`${BASE_URL}/return_keys`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ name_return: employeeName, key_return: employeeKey })  // názvy musia sedieť s backendom
    })
        .then(response => response.json())  // <-- Tu bol problém: chýbali zátvorky
        .then(
            reload_keys_database()
        )
        .catch(error => {
            console.error("Chyba pri požiadavke:", error);
            alert("Nastala chyba pri komunikácii so serverom.");
        });
}