function load_history(){
    fetch('https://localhost:5000/api/load_history')
    .then(response => response.text())
    .then(html => {
        document.getElementById("historyInfo").innerHTML = html;
    })
    .catch(error => {
        console.error("Chyba pri načítaní hostí:", error);
    });
}
