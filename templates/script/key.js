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

load_keys_database();