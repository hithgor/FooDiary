import {searchedDate} from './Datepicker-master/datepicker.js'


const cardContainer = document.getElementById('cardContainer')
const addMealButton = document.getElementById('addMealButton')
const loginHideShowDiv = document.getElementById('loginHideShowDiv')
const toggleLogin = document.getElementById('toggleLogin')
const bodyElement = document.getElementById('bodyId')
const todayBtn = document.getElementById('todayBtn')
const sendToDbBtn = document.getElementById('sendToDB')
const removeMealCardBtn = document.getElementById('removeMealCard')


var inputDate = searchedDate;
var today = new Date().toISOString().substring(0, 10);
const localStorageMealCards = JSON.parse(
    localStorage.getItem('mealCards')
  );

let mealCards =
    localStorage.getItem('mealCards') !== null ? localStorageMealCards : [];

var mealNumber = mealCards.length



function generateID() {
    return Math.floor(Math.random() * 100000000);
  }

function addMealCard() {
    mealNumber = mealCards.length
    const mealCard = {
    id: generateID(),
    user: "",
    dateCreated: searchedDate,
    number: mealNumber,
    mealTitle: "whatever",
    namesCalories: {name: "egg",
                    energy: 55},
    };

    mealCards.push(mealCard);
    addMealCardDOM(mealCard);

    updateLocalStorage();
    init();
}

function responseToObjectCreator(arrayOfObjects) {
    var arr = arrayOfObjects;
    console.log(arr);
    for (var i = 0; i < arr.length; i++) {
        var result = {
            id: 0,
            user: "",
            dateCreated: today,
            number: 0,
            mealTitle: "whatever",
            namesCalories: {name: "egg",
                            energy: 55},
        };
    
        result.id = arr[i].id;
        result.number = arr[i].number;
        result.dateCreated = arr[i].dateCreated
        mealCards.push(result);
    };
    updateLocalStorage();
    init();
    }

function fetchMealCardsByDay(targetDay) {
    const payload = {
        dateCreated: targetDay
    };
    console.log("tryin to send: " + JSON.stringify(payload));
    fetch('http://127.0.0.1:8000/caloriestracker/getMealCards/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify(payload),
    })
    .then((response) => response.status == 401 ? toggleLog() : response)
    .then((response) => response.json())
    ///.then((response) => console.log(response))
    .then((data) => responseToObjectCreator(data))
    .catch((error) => {
    console.error('Error: ', error);
    if(error===401) {
        toggleLog();
    }
    });
}

function filterMealCardsByDay(inputDate) {
    console.log("sending: " + inputDate)
    mealCards = [];
    clearCardContainerDOM();
    fetchMealCardsByDay(inputDate);

}

function removeMealCard(id) {
    mealCards = mealCards.filter(mealCard => mealCard.id !== id);
    mealCards.forEach(mealCardNumberIndexer)
    updateLocalStorage();
    init();
}
window.removeMealCard = removeMealCard;


  
function addMealCardDOM(mealCard) {

    const item = document.createElement('div');
    
    item.innerHTML = `
    <div id="mealCard" class="card mb-3" style="max-width: 18rem;">
        <div class="card-header">
            <h4 class="meal-number">Meal ${mealCard.number}</h4>
            <h5 class="card-title">${mealCard.mealTitle}</h5>
            <h5 id="MCid">${mealCard.id}</h5>
        </div>
        <div class="card-body cardFlexContainer">
            <p class="card-text-name">${mealCard.namesCalories.name}</p>
            <p class="card-text-calories">${mealCard.namesCalories.energy}</p>
            <button class="btn-outline-secondary btn-sm remove-meal">X</button>
        </div>
        <div class="card-body-add-position">
            <button class="btn-secondary btn-sm" id="add-meal-button">Add a meal</button>
            <button class="delete-btn btn-secondary" id="removeMealCard" onclick="removeMealCard(${mealCard.id})">x</button>
        </div>
    </div>

    `
    cardContainer.appendChild(item);
}

function clearCardContainerDOM() {
    cardContainer.innerHTML = ``
}


function updateLocalStorage() {
    localStorage.setItem('mealCards', JSON.stringify(mealCards));
  }
 
  
function mealCardNumberIndexer(mealCard) {
    mealCard.number = mealCards.indexOf(mealCard);
}
  
function sendToDb(data) {
    updateLocalStorage();
    console.log(data);
    console.log("tryin to send what's below");
    console.log(JSON.stringify(data));
    fetch('http://127.0.0.1:8000/caloriestracker/postSaveMealCards/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify(data),
    })
    ///.then((response) => response.json())
    .then((response) => response.status == 401 ? toggleLog() : false)
    .catch((error) => {
    console.error('Error: ', error);
    if(error===401) {
        toggleLog();
    }
    });
    
}



function init() {
    clearCardContainerDOM();
    mealCards.forEach(addMealCardDOM);
  }
init();


function toggleLog() {
    loginHideShowDiv.classList.toggle('hidden');
}


bodyElement.addEventListener('click', e => 
    e.target == loginHideShowDiv ? loginHideShowDiv.classList.remove('hidden') : false
  );

todayBtn.addEventListener('click', function() {
    
    filterMealCardsByDay(searchedDate);
});

addMealButton.addEventListener('click', function() {
    addMealCard();
})

sendToDbBtn.addEventListener('click', function() {
    sendToDb(mealCards);
})


toggleLogin.addEventListener('click', function() {
    toggleLog();
})

