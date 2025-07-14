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
        load_guests_table()
        return
    }

    console.log(search_input)

    fetch('http://localhost:5000/search_guests', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({search_input})  // Kratšia verzia zápisu (ES6)
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("personInfo").innerHTML = html;
    })
    .catch(console.error)

    document.getElementById("search_input_guests").value = ""
}

function delete_guest_button()
{
    delete_input = prompt("Priložte kartu")

    fetch('http://localhost:5000/delete_guests', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({delete_input})  // Kratšia verzia zápisu (ES6)
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("personInfo").innerHTML = html;
    })
    .catch(console.error)

    load_guests_table();
}

load_guests_table();