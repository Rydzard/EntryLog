function load_guests_table() {
    fetch('http://localhost:5000/api/load_guests')
    .then(response => response.text())
    .then(html => {
        document.getElementById("personInfo").innerHTML = html;
    })
    .catch(error => {
        console.error("Chyba pri načítaní hostí:", error);
    });
}

function search_guest_button() {
    var search_input = document.getElementById("search_input_guests").value.trim();

    if (!search_input) {
        load_guests_table()
        return
    }

    fetch(`http://localhost:5000/api/search_guests?search_input=${encodeURIComponent(search_input)}`, {
        method: 'GET'
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("personInfo").innerHTML = html;
    })
    .catch(console.error)
}

function delete_guest_button() {
    delete_input = prompt("Priložte kartu")

    if(!delete_input){
        alert("Ste nezadali čip karty")
        return
    }

    fetch('http://localhost:5000/api/delete_guests', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ delete_input })  // Kratšia verzia zápisu (ES6)
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("personInfo").innerHTML = html;
    })
    .catch(console.error)

    load_guests_table();
}

load_guests_table();