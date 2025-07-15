function searchEmployee()
{
    var input_string = document.getElementById("name_id").value.trim()

    if(!input_string){
        input_string = prompt("Zadajte čip").trim();
        input_string = parseInt(input_string);
    }

    console.log(input_string)

    fetch('http://localhost:5000/render_employee', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input_string })  // Kratšia verzia zápisu (ES6)
    })
    .then(response => response.json())
    .then(data => { 
        var meno = data[0].name;
        var čip = data[0].chip;
        var pracovisko = data[0].department;
        const myWindow = window.open("", "", "width=800,height=500");

        const cssURL = "styles/style.css"; // napr. "./moj-styl.css" ak je lokálne

        // Vytvoríme <link> pre CSS a pridáme ho do <head> nového okna
        const link = myWindow.document.createElement("link");
        link.rel = "stylesheet";
        link.href = cssURL;
        myWindow.document.head.appendChild(link);

        myWindow.document.body.innerHTML = "<h1>Info zamestnanca</h1> <br> <p> Meno:"+meno+"</p> <br> <p>Čip:"+ čip + 
                                            "</p> <br> <p>Pracovisko:" + pracovisko + "</p> <br>" + data[0].keys_table;

    })
    .catch(console.error);  // Zobrazíme chybu, ak nejaká nastane


}