function load_history()
{
    fetch('http://localhost:5000/load_history')
        .then(response => response.text())
        .then(html => {
            document.getElementById("historyInfo").innerHTML = html;
        })
        .catch(error => {
            console.error("Chyba pri načítaní hostí:", error);
        });
}

load_history();