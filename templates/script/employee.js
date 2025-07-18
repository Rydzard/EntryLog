function searchEmployee() {
    var input_string = document.getElementById("name_id").value.trim();

    if (!input_string) {
        console.log("Voslo sem int");
        input_string = prompt("Zadajte čip").trim();
        input_string = parseInt(input_string);
        console.log(input_string);
    }

    if (!input_string) {
        alert("Ste nezadali žiaden vstup, je potrebné meno zamestnanca alebo číslo čipu");
        return;
    }

    console.log(input_string);


    const url = `http://localhost:5000/api/render_employee?search_input=${encodeURIComponent(input_string)}`;

    fetch(url, {
        method: 'GET'
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            var meno = data.name;
            console.log(meno)
            var cip = data.chip;
            var pracovisko = data.department;

            const myWindow = window.open("", "", "width=800,height=500");
            const cssURL = "styles/style.css";

            const link = myWindow.document.createElement("link");
            link.rel = "stylesheet";
            link.href = cssURL;
            myWindow.document.head.appendChild(link);

            myWindow.document.body.innerHTML = "<h1>Info zamestnanca</h1> <br> <p>Meno: " + meno + "</p> <br> <p>Čip: " + cip +
                "</p> <br> <p>Pracovisko: " + pracovisko + "</p> <br>" +
                '<div id="personInfo" class="personInfo">' + data.keys_table + '</div>';
        })
        .catch(error => {
            console.error("Chyba pri fetchnutí:", error);
        });

}

function toggleSpecialInputs() {
    const isChecked = document.getElementById('special_checkbox').checked;
    document.getElementById('date_id').disabled = !isChecked;
    document.getElementById('why_id').disabled = !isChecked;
}

function add_key() {
    var name = document.getElementById('name').value;
    var key = document.getElementById('key').value;
    var date = document.getElementById('date_id').value;
    var why = document.getElementById('why_id').value;
    const isChecked = document.getElementById('special_checkbox').checked;

    if (!name || !key) {
        alert("Treba vyplniť celý dotazník");
        return;
    }

    if (key <= 0) {
        alert("Ste zadali záporné čislo klúča");
        return;
    }

    if (!isChecked) {
        why = "Nepriradené"
        date = "Nepriradené"
    }

    fetch('http://localhost:5000/api/add_key', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, key, date_id: date, why_id: why })  // názvy musia sedieť s backendom
    })
        .then(response => response.json())  // ← opravene: voláme json ako funkciu
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

function return_key() {
    var name = document.getElementById('name_return').value;
    var key = document.getElementById('key_return').value;

    if (!name) {
        var chip = prompt("Zadajte čip zamestnanca ");
    }

    if (chip.length !== 10) {
        alert("Nesprávny počet čísel");
        return;
    }

    if (!key) {
        alert("Treba vyplniť celý dotazník");
        return;
    }

    if (key <= 0) {
        alert("Ste zadali záporné čislo klúča");
        return;
    }

    fetch('http://localhost:5000/api/return_keys', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
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

