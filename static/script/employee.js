
function searchEmployee() {
    //načíta vstup
    var input_string = document.getElementById("name_id").value.trim();

    //ak nezadal vstup,tak nech načita čip
    if (!input_string) {
        input_string = prompt("Zadajte čip").trim();
        input_string = parseInt(input_string);
    }

    //aj napriem tomu že nič nezdal tak vyhodi alert s chybou a da return
    if (!input_string) {
        alert("Ste nezadali žiaden vstup, je potrebné meno zamestnanca alebo číslo čipu");
        return;
    }

    //url kde sa bude posielat sprava na api
    const url = `${BASE_URL}/render_employee?search_input=${encodeURIComponent(input_string)}`;

    fetch(url, {
        method: 'GET',
        credentials: 'include'
    })
        .then(response => {
            if (response.status === 401) {
                alert("Nie si prihlásený alebo tvoja session vypršala.");
                throw new Error("Unauthorized");
            }

            if (response.status === 404) {
                alert("Zamestnanec neexistuje");
                throw new Error("Unauthorized");
            }

            return response.json();
        })
        .then(data => {
            var name_json = data.name;
            var chip_json = data.chip;
            var department_json = data.department;

            //otvorí nové okno s velkostou a nastaví subor css ktorý sa otovrí pre toto okno
            const myWindow = window.open("", "", "width=1400,height=700");
            const cssURL = "static/styles/window.css";

            //tu sa ešte všetko pridá css na začiatok html
            const link = myWindow.document.createElement("link");
            link.rel = "stylesheet";
            link.href = cssURL;
            myWindow.document.head.appendChild(link);

            //pridanie body elementov a informacii o zamestnancovi a klúčov
            myWindow.document.body.innerHTML = `
                                                <div class="employee-card">
                                                    <h1>Info zamestnanca</h1>
                                                    <p><strong>Meno:</strong> <span>${name_json}</span></p>
                                                    <p><strong>Čip:</strong> <span>${chip_json}</span></p>
                                                    <p><strong>Pracovisko:</strong> <span>${department_json}</span></p>
                                                </div>
                                                <div id="personInfo" class="personInfo">
                                                    ${data.keys_table}
                                                </div>
                                            `;
        })
        .catch(error => {
            console.error("Chyba pri fetchnutí:", error);
        });

}

//funckia ktora zabraví inputy pre ked je zaškrtnute special checkbox
function toggleSpecialInputs() {
    const isChecked = document.getElementById('special_checkbox').checked;
    document.getElementById('date_id').disabled = !isChecked;
    document.getElementById('why_id').disabled = !isChecked;
    document.getElementById('time_id').disabled = !isChecked;
}


//funkcia ktorá pridáva klúče zamestnancom
function add_key() {

    //vstupy
    var name = document.getElementById('name').value;
    var key = document.getElementById('key').value;
    var date = document.getElementById('date_id').value;
    var time = document.getElementById('time_id').value;
    var why = document.getElementById('why_id').value;
    const isChecked = document.getElementById('special_checkbox').checked;

    //spracovanie dátumu
    var parts = date.split('-');
    var formattedDate = parts[2] + '.' + parts[1] + '.' + parts[0];
    formattedDate = formattedDate + ' ' + time;
    //ak nezadal vstupy tak vyhodi alert a vráti return
    if (!name || !key) {
        alert("Treba vyplniť celý dotazník");
        return;
    }

    //ak zadá ručne zaporné čislo do inputu tak vyhodi alert a vráti return
    if (key <= 0) {
        alert("Ste zadali záporné čislo klúča");
        return;
    }

    if(isChecked && !date && !why && !time){
        alert("Ste zadali nepriradené dátum,čas alebo prečo");
        return;
    }

    //ak vátnik nič nezadal tak nastavi dátum a prečo ako nepriradené
    if (!isChecked) {
        why = "Nepriradené"
        formattedDate = "Nepriradené"
    }

    fetch(`${BASE_URL}/add_key`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ name, key, date_id: formattedDate, why_id: why })
    })
        .then(response => response.json())  // bez zložených zátvoriek, alebo s explicitným return
        .then(data => alert(data.message))
        .catch(error => {
            console.error("Chyba pri požiadavke:", error);
            alert("Nastala chyba pri komunikácii so serverom.");
        });
}

function return_key() {
    var name = document.getElementById('name_return').value;
    var key = document.getElementById('key_return').value;
    var chip;

    if (!key) {
        alert("Treba vyplniť celý dotazník (aspoň kľúč)");
        return;
    }

    if (key <= 0) {
        alert("Ste zadali záporné čislo klúča");
        return;
    }


    if (!name) {
        chip = prompt("Zadajte čip zamestnanca ");

        // Skontroluj, či čip existuje a má presne 10 znakov
        if (chip.length !== 10) {
            alert("Nesprávny počet čísel");
            return;
        }
    }

    fetch(`${BASE_URL}/return_keys`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ name_return: name, key_return: key, chip_return: chip })  // názvy musia sedieť s backendom
    })
        .then(response => response.json())  // <-- Tu bol problém: chýbali zátvorky
        .then(data => {
            if (data.status === "success") {
                alert(data.message);
            } else {
                alert("Chyba: " + data.message);
            }
        })
        .catch(error => {
            console.error("Chyba pri požiadavke:", error);
            alert("Nastala chyba pri komunikácii so serverom.");
        });
}

