const app = document.getElementById('app');

const styleLink = document.getElementById('page-style');

function render() {
  const hash = location.hash.slice(1);

  changeCSS(hash);

  if (hash === 'registration') {
    app.innerHTML = registrationContent;
  } else if (hash === 'index') {
    app.innerHTML = indexContent;
    load_guests_table();
  } else if (hash === 'employee') {
    app.innerHTML = employeeContent;
  } else if (hash === 'keys') {
    app.innerHTML = keyContent;
    load_keys_database();
  } else if (hash === 'history') {
    app.innerHTML = historyContent;
    load_history();
  } else {
    app.innerHTML = '<h1>Vitajte</h1><p>Vyberte položku z menu.</p>';
  }
}


function changeCSS(hash) {
  const cssMap = {
    registration: 'templates/styles/registration.css',
    index: 'templates/styles/style.css',
    employee: 'templates/styles/employee.css',
    keys: 'templates/styles/keys.css',
    history: 'templates/styles/history.css'
  };

  // nastav štýl podľa hash, inak default
  styleLink.href = cssMap[hash] || 'templates/styles/style.css';
}

window.addEventListener('hashchange', render);
window.addEventListener('load', render);


const indexContent = `
        <div id="personInfo" class="personInfo">

        </div>

    <br>

        <div>
            <br><br>
            <p>Vyhľadať návštevníka(Meno)</p><br>
            <input id="search_input_guests"> <button onclick="search_guest_button()">Hľadať návštevníka</button>

            <br><br>
            <p>Vymazať návštevníka (Čip)</p><br>
            <button onclick="delete_guest_button()">Vymazať návštevníka</button>
        </div>`;

const employeeContent = ` 

        <div>
            <p>
                <label>
                    <input type="checkbox" id="special_checkbox" onchange="toggleSpecialInputs()">
                    Špeciálne vydanie
                </label>
            </p>

            <p>Meno</p>
            <input id="name" type="text">

            <p>číslo klúču</p>
            <input id="key" type="number">

            <p>Do kedy</p>
            <input type="date" id="date_id" disabled>

            <p>Prečo</p>
            <input type="text" id="why_id" disabled>

            <button onclick="add_key()">Pridať kluč zamestnancovi</button>
        </div>

        <div>
            <p>Meno zamestnanca (nepovinne)</p>
            <input id="name_id" type="text">
            <button onclick="searchEmployee()">Hľadať zamestnanca</button>
        </div>

        <div>
            <p>Meno zamestnanca (nepovinne)</p>
            <input type="text" id="name_return">
            <p>číslo klúču</p>
            <input type="number" id="key_return" min="1">
            <br>
            <button onclick="return_key()">Vrátiť klúče</button>
        </div>
       `;
const historyContent = `
    <div id="historyInfo" class="historyInfo">

    </div>`;
const keyContent = `        
          <div id="historyInfo" class="historyInfo">

          </div>

          <p>Najsť klúč</p>
          <input type="number" id="search_key_id" min="1">
          <button id="search_button_id" onclick="search_key()">Nájsť klúč</button>
`;
const registrationContent = ` 
         <div>
            <p>Meno</p>
            <input id="name_id"> 

            <p>Za kým</p>
            <input id="who_id"> 

            <p>Do kedy</p>
            <input type="date" id="date_id"> 
            
            <p>Prečo</p>
            <select id="why_id">
                <option value="Návšteva">Návšteva</option>
                <option value="Pohovor">Pohovor</option>
            </select> 
            <button onclick="add_guest()">Pridať návštevníka</button>
        </div>`;
