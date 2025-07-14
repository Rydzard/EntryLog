function searchEmployee()
{
    console.log("Vosiel")

    var input = document.getElementById("name_id").value.trim()
    if(!input)
    {
        chip = prompt("Priložte kartu")
    }

    const myWindow = window.open("", "", "width=800,height=500");
    myWindow.document.body.innerHTML = "<h1>Info zamestnanca</h1> <br><br> <p>"+ input + " " + chip + "</p>"
}