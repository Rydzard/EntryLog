function load_history(){
    fetch('https://localhost:5000/api/load_history')
    .then(response => {
        if (response.status === 401) {
            alert("Nie si prihlásený alebo tvoja session vypršala.");
            throw new Error("Unauthorized");
        }
        
        return response.text()})
    .then(html => {
        document.getElementById("historyInfo").innerHTML = html;
    })
    .catch(error => {
        console.error("Chyba pri načítaní hostí:", error);
    });
}


function searchHistory(){

    var name = document.getElementById("search_name_id").value.trim();

    if (!name) {
        load_history()
        return
    }

    fetch('https://localhost:5000/api/search_on_history', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ name })  // Kratšia verzia zápisu (ES6)
    })
    .then(response => {
        if (response.status === 401) {
            alert("Nie si prihlásený alebo tvoja session vypršala.");
            throw new Error("Unauthorized");
        }
        return response.text();
    })
    .then(html => {
        const container = document.getElementById("historyInfo");
        container.innerHTML = html;
    })
    .catch(console.error);
}

function search_key_history(){

    var search_key_id = document.getElementById("search_key_id").value.trim();

    if(!search_key_id){
        load_history_keys()
        return
    }

    fetch('https://localhost:5000/api/search_employee_on_history', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ search_key_id })  // Kratšia verzia zápisu (ES6)
    })
    .then(response => {
        if (response.status === 401) {
            alert("Nie si prihlásený alebo tvoja session vypršala.");
            throw new Error("Unauthorized");
        }
        return response.text();
    })
    .then(html => {
        const container = document.getElementById("historyInfo");
        container.innerHTML = html;
    })
    .catch(console.error);
}