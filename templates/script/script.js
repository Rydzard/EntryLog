function add_guest()
{

    // získanie údajov zo vstupu
    var name = document.getElementById("name_id").value.trim();
    var who = document.getElementById("who_id").value.trim();
    var date = document.getElementById("date_id").value.trim();
    var why = document.getElementById("why_id").value.trim();

    // overenie vstupov
    if (!name || !who || !date || !why) {
        alert("Zadaj všetky povinné údaje (meno, kto pozval, dátum a dôvod)");
        return; // zastaví funkciu, ak údaje chýbajú
    }

    // Poslanie dát na server pomocou fetch
    fetch('http://localhost:5000/add_guest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name , who, date, why })  // Kratšia verzia zápisu (ES6)
    })
    .then(response => response.json())
    .then(data => alert(data.message))  // Zobrazíme správu zo servera
    .catch(console.error);  // Zobrazíme chybu, ak nejaká nastane

    var table = document.getElementById("table_of_guests");

    var row = table.insertRow(1);

    // Insert new cells (<td> elements) at the 1st and 2nd position of the "new" <tr> element:
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    var cell5 = row.insertCell(4);

    cell1.innerHTML = name;
    cell2.innerHTML = who;
    cell3.innerHTML = date;
    cell4.innerHTML = why;
    cell5.innerHTML = "<td><button onclick=" + "showOptions() " +" class=" + "moreButton" + ">...</button></td>"
}

function load_guests_table()
{
    fetch('http://localhost:5000/load_guests')
        .then(response => response.text())
        .then(html => {
            document.getElementById("personInfo").innerHTML = html;
        })
        .catch(error => {
            console.error("Chyba pri načítaní hostí:", error);
        });
}

function showOptions()
{
    console.log("Bla bla")
}

function search_guest_button(){
    var search_input = document.getElementById("search_input_guests").value.trim();

    if(!search_input)
    {
       return alert("Treba pridat do searchu meno zamestnanca")
    }

    console.log(search_input)

    fetch('http://localhost:5000/search_guests', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({search_input})  // Kratšia verzia zápisu (ES6)
    })
    .then(response => response.json())
    .catch(console.error)
}

load_guests_table();