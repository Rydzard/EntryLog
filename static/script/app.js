const app = document.getElementById('app');

const styleLink = document.getElementById('page-style');

function render() {
  const hash = location.hash.slice(1);

  changeCSS(hash);

  if (hash === 'registration') {
    app.innerHTML = registrationContent;
  } else if (hash === 'guests') {
    app.innerHTML = guestsContent;
    load_guests_table();
  } else if (hash === 'employees') {
    app.innerHTML = employeeContent;
  } else if (hash === 'keys') {
    app.innerHTML = keyContent;
    load_keys_database();
  } else if (hash === 'history') {
    app.innerHTML = historyContent;
    load_history();
  } else if (hash ==='history_keys'){
    app.innerHTML = historyKeysContent;
    load_history_keys();
  } else {
    app.innerHTML = login;
    isLoggedIn = false;
  }
}

function changeCSS(hash) {
  const cssMap = {
    registration: '../static/styles/registration.css',
    guests: '../static/styles/style.css',
    employees: '../static/styles/employee.css',
    keys: '../static/styles/keys.css',
    history: '../static/styles/history.css',
    history_keys:'../static/styles/history.css'
  };

  // nastav štýl podľa hash, inak default
  styleLink.href = cssMap[hash] || '../static/styles/login.css';
}

window.addEventListener('hashchange', render);
window.addEventListener('load', render);


const login = `
            <div class="login-box">
               <h2>Prihlásenie</h2>

               <label for="input_login_1">Meno a priezvisko vrátnika</label>
               <input class="styled-input" id="input_login_1" type="text" placeholder="Meno a priezvisko">

               <label for="input_login_2">Čip vrátnika</label>
               <input class="styled-input" id="input_login_2" type="password" placeholder="Čip v tvare '000123567'">

               <button id="search_button_id" onclick="login_fun()">Prihlásiť sa</button>
          </div>`;


const guestsContent = `
        <div id="personInfo" class="personInfo">

        </div>

        <br>

        <div>
            <br><br>
            <div class="delete-guest-box">
            <p>Vyhľadať návštevníka(Meno)</p><br>
            <input class="styled-input" id="search_input_guests"> 
            <button onclick="search_guest_button()">Hľadať návštevníka</button>
            <br><br>

              <p>Vymazať návštevníka (Čip)</p>
              <button onclick="delete_guest_button()">Vymazať návštevníka</button>

            </div>
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

            <p>DôvodDôvod</p>
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

          <div class="find-key-box">
            <p>Najsť klúč</p>
            <input type="number" class="styled-input" id="search_key_id" min="1">
            <button id="search_button_id" onclick="search_key()">Nájsť klúč</button>
          </div>
`;
const registrationContent = ` 
         <div>
            <p>Meno</p>
            <input id="name_id"> 

            <p>Za kým</p>
            <input id="who_id"> 

            <p>Do kedy</p>
            <input type="date" id="date_id"> 
            <input type="time" id="time_id">
            
            <p>Dôvod</p>
            <select id="why_id">
                <option value="Návšteva">Návšteva</option>
                <option value="Pohovor">Pohovor</option>
            </select> 

            <br>
              <p>
                <label>
                    <input type="checkbox" id="registration_checkbox">
                    Bez čipu
                </label>
              </p>
            <br>
            <button onclick="add_guest()">Pridať návštevníka</button>

        </div>`;

const historyKeysContent = `
    <div id="historyInfo" class="historyInfo">

    </div>`;

function login_fun() {
  //získanie údajov z formularú Login
  name_guard = document.getElementById('input_login_1').value;
  chip = document.getElementById('input_login_2').value;

  //skontrola, či sú všetky údaje zadane
  if (!name_guard && !chip) {
    alert('Nezadali ste všetky údaje')
    return;
  }

  //fetch request na server, ktorý vráti odpoveď o zalogovaní
  fetch('https://localhost:5000/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ name_guard, chip })  // Kratšia verzia zápisu (ES6)
  })
    .then(response => response.json())
    .then(data => {
      //ak vráti status "success", tak nastavíme isLoggedIn na true a nastavi stránku na zadávanie klúčov
      if (data.status === "success") {
        window.location.href = "#keys";
        isLoggedIn = true;
      }
      else {
        alert(data.message)
      }
    }) // Zobrazíme správu zo servera
    .catch(console.error);  // Zobrazíme chybu, ak nejaká nastane

};


//Nastavenie že ak používatel nie je prihlásený, tak nevie listovat v odkazoch
document.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', function (e) {
    if (!isLoggedIn) {
      e.preventDefault();
      alert("Najprv sa musíš prihlásiť.");
    }
  });
});


function logout(event) {
  event.preventDefault(); // Zastaví reload stránky

  fetch('https://localhost:5000/api/logout')
    .then(response => {
      if (!response.ok) throw new Error("Network response was not ok");
      // Nepotrebujeme parsovať JSON, stačí úspešná odpoveď
      window.location.href = "/"; // presmeruj na login stránku
    })
    .catch(error => {
      console.error('Logout error:', error);
    });
}