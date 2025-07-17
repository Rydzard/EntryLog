function load_keys_database() {
     fetch('http://localhost:5000/load_keys_database')
          .then(response => response.text())
          .then(html => {
               document.getElementById("historyInfo").innerHTML = html;
          })
          .catch(error => {
               console.error("Chyba pri načítaní hostí:", error);
          });
}

function search_key() {
     console.log("Voslo sem")
     var key_number = document.getElementById("search_key_id").value;
     console.log(key_number)

    if(!key_number)
    {
        load_keys_database()
        return
    }

    fetch('http://localhost:5000/search_key', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({key_number})  // Kratšia verzia zápisu (ES6)
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("historyInfo").innerHTML = html;
    })
    .catch(console.error)

    document.getElementById("search_input_guests").value = ""
}


load_keys_database();