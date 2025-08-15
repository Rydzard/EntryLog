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
