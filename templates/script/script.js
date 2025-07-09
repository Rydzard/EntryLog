function addInfo()
{

    //získanie údajov zo vstupu
    var name = document.getElementById("name_id").value;
    var who = document.getElementById("who_id").value;
    var date = document.getElementById("date_id").value;
    var why = document.getElementById("why_id").value;

    // Poslanie dát na server pomocou fetch
    fetch('localhost:5000/process_data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name , who, date, why })  // Kratšia verzia zápisu (ES6)
    })
    .then(response => response.json())
    .then(data => alert(data.message))  // Zobrazíme správu zo servera
    .catch(console.error);  // Zobrazíme chybu, ak nejaká nastane

}

function showOptions()
{
    console.log("Bla bla")
}