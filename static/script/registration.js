
function add_guest() {
    // získanie údajov zo vstupu
    var name = document.getElementById("name_id").value.trim();
    var who = document.getElementById("who_id").value.trim();
    var dateStr = document.getElementById("date_id").value.trim();
    var why = document.getElementById("why_id").value.trim();
    var currentTime = getCurrentTime().toString();
    var time = document.getElementById("time_id").value.trim();

    // overenie vstupov
    if (!name || !currentTime || !who || !dateStr || !why || !time) {
        alert("Zadaj všetky povinné údaje (meno, kto pozval, dátum a dôvod)");
        return; // zastaví funkciu, ak údaje chýbajú
    }

    // prevod reťazca na objekt Date
    var date = new Date(dateStr);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
    const year = date.getFullYear();

    var formattedDate = `${day}.${month}.${year} ${time}`;

    const isChecked = document.getElementById('registration_checkbox').checked;


    if (!isChecked) {
        chip = prompt("Priložte kartu")

        if (!chip || (chip && chip.length !== 10)) {
            alert("Nesprávne zadali kartu")
            return;
        }
    }

    else {
        chip = "Nepridané"
    }

    // Poslanie dát na server pomocou fetch
    fetch(`${BASE_URL}/add_guest`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ name, who, currentTime, formattedDate, why, chip })  // Kratšia verzia zápisu (ES6)
    })
        .then(response => {
            if (response.status === 401) {
                alert("Nie si prihlásený alebo tvoja session vypršala.");
                throw new Error("Unauthorized");
            }
            return response.json();
        })
        .then(data => alert(data.message))  // Zobrazíme správu zo servera
        .catch(console.error);  // Zobrazíme chybu, ak nejaká nastane
}

function getCurrentTime() {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    var hh = String(today.getHours()).padStart(2, '0');
    var min = String(today.getMinutes()).padStart(2, '0');

    return dd + "." + mm + "." + yyyy + " " + hh + ":" + min;
}