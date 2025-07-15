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

function showOptions(id) {
    fetch('http://localhost:5000/show_options', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id })
    })
    .then(response => response.json())  // Spracovanie ako JSON
    .then(data => {
        console.log("Parsed JSON data:", data);
        var meno = data[0].name;
        var čip = data[0].chip;

        const myWindow = window.open("", "", "width=800,height=500");

        const cssURL = "styles/style.css"; 

        const link = myWindow.document.createElement("link");
        link.rel = "stylesheet";
        link.href = cssURL;
        myWindow.document.head.appendChild(link);

        myWindow.document.body.innerHTML = "<h1>Info návštevníka</h1> <br> <p> Meno:" + meno + "</p> <br> <p>Čip:" + čip + 
                                            "</p> <br>" + data[0].keys_table;
    })
    .catch(console.error);
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