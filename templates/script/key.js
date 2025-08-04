function load_keys_database() {
    fetch('http://localhost:5000/api/load_keys_database')
    .then(response => response.text())
    .then(html => {
        document.getElementById("historyInfo").innerHTML = html;
    })
    .catch(error => {
        console.error("Chyba pri načítaní hostí:", error);
    });
}

function search_key() {
     var key_number = document.getElementById("search_key_id").value;

    if(!key_number){
        load_keys_database()
        return
    }
    
    if(key_number <= 0){
        alert("Zadejte číslo klíče")
        return
    }

    fetch(`http://localhost:5000/api/search_key?key_number=${encodeURIComponent(key_number)}`, {
        method: 'GET'
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById("historyInfo").innerHTML = html;
    })
    .catch(console.error)
}


load_keys_database();