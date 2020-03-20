import {searchedDate} from './Datepicker-master/datepicker.js'

const cardContainer = document.getElementById('cardContainer')
const addMealButton = document.getElementById('addMealButton')
const loginHideShowDiv = document.getElementById('loginHideShowDiv')
const toggleLogin = document.getElementById('toggleLogin')
const bodyElement = document.getElementById('bodyId')
const todayBtn = document.getElementById('todayBtn')
const sendToDbBtn = document.getElementById('sendToDB')
const removeMealCardBtn = document.getElementById('removeMealCard')


////Functions associated with those to variables need to be refactored into class for modularity
var IngredientNameHelper = "";
var IngredientCaloriesHelper = 0;
///End


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
    namesCalories: [{name: "egg", energy: 55}, {name: "banana", energy: 110}]
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
            namesCalories: {name: "egg", energy: 56},

        };
    
        result.id = arr[i].id;
        result.number = arr[i].number;
        result.dateCreated = arr[i].dateCreated;
        result.namesCalories = arr[i].namesCalories;

        mealCards.push(result);
    };
    updateLocalStorage();
    init();
    }

function nutritionixAPI(mealCardNumber) {
    var searchedFood = document.getElementById(`searchFoodNameInput${mealCardNumber}`).value;
    fetch(`https://api.nal.usda.gov/fdc/v1/search?api_key=tkjynWdwgrZk4ZSFXGK43b36n34uLXnY5aUQsWWc&generalSearchInput=${searchedFood}`)
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        populateDropdownWithFoodOptions(searchedFood);
    })
}

//// Refactor below into: send fetch to database, database sends request, saves json, gets calories from major nutrients, builds a response of {name: egg, calories: 55} and gives it back here
function getIngredientFromId() {
    let dropdown = document.getElementById('locality-dropdown')
    var idToSearch = dropdown.options[dropdown.selectedIndex].value;
    IngredientNameHelper = dropdown.options[dropdown.selectedIndex].text;
    const payload = {
        reqIngredientId:  idToSearch
    }
    fetch(`http://127.0.0.1:8000/caloriestracker/getIngredientFromId/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(payload),
    })
    .then((response) => response.json())
    .then((data) => {
        console.log("Below is the full response from getIngredientFromId");
        console.log(data);
        ///Consume data into populating portion sizes in a form
        populateDropdownWithPortionSizes(data);
    });
}

function appendIngredientToMealCard(id, ingredientName, ingredientCalories) {
    let targetMealCard = mealCards.filter(mealCard => mealCard.id == id)[0];
    
    let ingredientToAppend = {
        name: ingredientName, 
        energy: ingredientCalories};

    targetMealCard.namesCalories.push(ingredientToAppend);
    updateLocalStorage();
    sumCaloriesOfTheDay(id)
    init();
}

function sumCaloriesOfTheDay(id) {
    let targetMealCard = mealCards.filter(mealCard => mealCard.id == id)[0];
    let arr = targetMealCard.namesCalories;
    let sumOfCalories = 0;
    for(var i = 0; i < arr.length; i++) {
        sumOfCalories = sumOfCalories + parseInt(arr[i].energy);
    };
    return sumOfCalories;
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
window.nutritionixAPI = nutritionixAPI;
window.getIngredientFromId = getIngredientFromId;

function addMealCardDOM(mealCard) {
    /// Creating mealCard template from given payload
    const item = document.createElement('div');
    
    item.innerHTML = `
    <div id="mealCard" class="card card2 mb-3">
        <div>
            <button class="delete-btn btn-secondary" id="removeMealCard" onclick="removeMealCard(${mealCard.id})">x</button>
            <div class="card-header">
                <h4 class="meal-number">Meal ${mealCard.number}</h4>
                <h5 class="card-title">${mealCard.mealTitle}</h5>
                <h5 id="MCid">${mealCard.id}</h5>
            </div>
            <div class="card-body cardFlexContainer" id="ingrdiv${mealCard.number}">

                <button class="btn-outline-secondary btn-sm remove-meal">X</button>
            </div>
            <div class="card-body-add-position">
                <span class="btn-sm
                spanFoodInvisible" id="showAddFoodBtn">+</span>
            </div>
        </div>

        <div id="addFoodForm" class="formIndex mb-3 formIndexInvisible">
            <button class="delete-btn btn-secondary" id="removeMealCard">x</button>
            <form>
                <h4 style="margin-top:1vh"> Food search </h4>
                <input placeholder="food name" id="searchFoodNameInput${mealCard.number}">
                <button type="button" class="btn-sm btn-search-food" id="nutritionixAddMeal" onclick="nutritionixAPI(${mealCard.number})">&#8627</button>
                <select id="locality-dropdown" class="dropdownChoice" name="locality" onchange="getIngredientFromId()"></select>
                <h4 style="margin-top:1vh"> Portion size </h4>
                <select id="food-portion-dropdown" class="dropdownChoice" name="foodPortion" placeholder="Pick a portion"></select>
                <h4 style="margin-top:1vh"> Quantity </h4>
                <input class="quantityFormInput" placeholder="0" id="ingredientQuantity" disabled><span class="quantityFormInputSpan">g</span>
                <span class="btn-lg quantityBtn quantityBtnLeft" id="QuantityMinus">-</span>
                <span class="btn-lg quantityBtn" id="QuantityPlus">+</span>
                <button class="btn-search-food btn-lg" id="addFoodFormBtn"
                type="submit"> &#8676;Add position
                </button><span class="btn-lg ingredientCaloriesSum" id="ingredientCaloriesSum">0kcal</span>
            </form>
        </div
    </div>
    `;


    ///Inserting food-calories pairs into ingrdiv above before creating mealcardDOM
    var whatever = item.querySelector(".card-body");
    whatever.innerHTML = ``;

    mealCard.namesCalories.forEach(function(item) {
        Object.keys(item).forEach(function(key) {
            const element = document.createElement('span');
            element.innerHTML = `
                            ${item[key]}
        `;
        whatever.appendChild(element);
        });
        
    });
    const element = document.createElement('span');
    element.innerText = `${sumCaloriesOfTheDay(mealCard.id)}`;
    whatever.appendChild(element);
 
    cardContainer.appendChild(item);
    const mealCardDomElement = document.getElementById('mealCard')
    const showAddFoodBtn = document.getElementById('showAddFoodBtn')
    const addFoodForm = document.getElementById('addFoodForm')

    mealCardDomElement.addEventListener('click', function() {
        mealCardDomElement.classList.add('clickedAndCentered');
        mealCardDomElement.classList.remove('card2');
        showAddFoodBtn.classList.add('spanFoodVisible');
        showAddFoodBtn.addEventListener('click', function() {
            addFoodForm.classList.remove('formIndexInvisible');
            addFoodForm.classList.add('formIndexVisible');
            ////adding ingredient to localStorage functionality
            let addFoodFormBtn = document.getElementById('addFoodFormBtn');
            let ingredientCaloriesSum = document.getElementById('ingredientCaloriesSum');
            
            addFoodFormBtn.addEventListener('click', function() {
                appendIngredientToMealCard(mealCard.id, IngredientNameHelper, IngredientCaloriesHelper);
            })
            ////end
        });
    });
    bodyElement.addEventListener('click', function(e) {
        e.target == bodyElement ? mealCardDomElement.classList.add('card2') : false;
        e.target == bodyElement ? mealCardDomElement.classList.remove('clickedAndCentered') : false;
        e.target == bodyElement ? showAddFoodBtn.classList.remove('spanFoodVisible') : false;
        e.target == bodyElement ? addFoodForm.classList.remove('formIndexVisible') : false;
        e.target == bodyElement ? addFoodForm.classList.add('formIndexInvisible') : false;
    } 
    );

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

//// Dropdown with food options logic - create all options from JSON, after choosing send to others
function populateDropdownWithFoodOptions(searchedFood) {
    let dropdown = document.getElementById('locality-dropdown');
    dropdown.length = 0;

    let defaultOption = document.createElement('option');
    defaultOption.text = 'Choose your food';

    dropdown.add(defaultOption);
    dropdown.selectedIndex = 0;

    const url = `https://api.nal.usda.gov/fdc/v1/search?api_key=tkjynWdwgrZk4ZSFXGK43b36n34uLXnY5aUQsWWc&generalSearchInput=${searchedFood}`;

    fetch(url)  
    .then(  
        function(response) {  
        if (response.status !== 200) {  
            console.warn('Looks like there was a problem. Status Code: ' + 
            response.status);  
            return;  
        }

        // Examine the text in the response  
        response.json().then(function(data) {  
            console.log("populating the dropdown");
            console.log(data);
            let option;
        
            for (let i = 0; i < data.foods.length; i++) {
            option = document.createElement('option');
            option.text = data.foods[i].description;
            option.value = data.foods[i].fdcId;
            dropdown.add(option);
            }    
        });  
        }  
    )  
    .catch(function(err) {  
        console.error('Fetch Error -', err);  
    });
}
///END OF DROPDOWN 


function populateDropdownWithPortionSizes(data) {
    let dropdown = document.getElementById('food-portion-dropdown');
    dropdown.length = 0;

    let defaultOption = document.createElement('option');
    defaultOption.text = 'Choose portion size';
    dropdown.add(defaultOption);

    // Examine the text in the response  
    console.log("populating the portionsize dropdown");
    console.log(data);
    let option;

    for (let i = 0; i < data.foodPortions.length; i++) {
        option = document.createElement('option');
        option.text = Object.values(data.foodPortions[i]) + "g " + "[" + Object.keys(data.foodPortions[i]) + "]";
        option.value = Object.values(data.foodPortions[i]);
        dropdown.add(option);
    }


    ///Adding event listeners for quantity management
    let ingredientQuantityInput = document.getElementById('ingredientQuantity');
    let quantityPlusBtn = document.getElementById('QuantityPlus');
    let quantityMinusBtn = document.getElementById('QuantityMinus');
    let ingredientCaloriesSum = document.getElementById('ingredientCaloriesSum');
    
    ///helpers for event listeners
    function populateIngredientCaloriesValue(data) {
        let caloriesPer100g = data.calories;
        let portionSizeMultiplier = parseInt(ingredientQuantityInput.value)*0.01;
        let finalIngredientCalories = (caloriesPer100g * portionSizeMultiplier).toFixed(0);
        ingredientCaloriesSum.textContent = `${finalIngredientCalories}kcal`;
        return IngredientCaloriesHelper = finalIngredientCalories;
    };


    dropdown.addEventListener('change', function() {
        if (dropdown.value) {
            ingredientQuantityInput.value = parseInt(dropdown.value);
            populateIngredientCaloriesValue(data);
        };
    });

    quantityPlusBtn.addEventListener('click', function() {
        ingredientQuantityInput.value = parseInt(ingredientQuantityInput.value) + parseInt(dropdown.value);
        populateIngredientCaloriesValue(data);
    });

    quantityMinusBtn.addEventListener('click', function() {
        if (ingredientQuantityInput.value > 0) {
            ingredientQuantityInput.value = parseInt(ingredientQuantityInput.value) - parseInt(dropdown.value);
            populateIngredientCaloriesValue(data);
        };
    });
    
}  



/// HELPER/STARTING FUNCTIONS
function init() {
    clearCardContainerDOM();
    mealCards.forEach(addMealCardDOM);
  }


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

