const packCheckBoxes = document.getElementsByName("packsIncluded[]");
const categoryCheckBoxes = document.getElementsByName("categoriesIncluded[]");
const checkBoxes = document.getElementsByClassName("checkBox");



//save whether settting checkbox is checked
function saveChoices(array) {
    array.forEach(function (checkBox) {
        localStorage.setItem(checkBox.id, checkBox.checked);
    })
}

//load checkbox last state and set
function load() {
    console.log(`Nice to see you down here! While you\'re poking around,
    listen to my favourite simlish song: https://www.youtube.com/watch?v=ZzlGgLoY3hQ
    and shoot me a message :)`);
    [].forEach.call(checkBoxes, function (checkBox) {
        let checked = JSON.parse(localStorage.getItem(checkBox.id));
        document.getElementById(checkBox.id).checked = checked;
    });
}

//check whether a settings checkbox in the group has been selected
function isChecked(array) {
    let notChecked = 0
    array.forEach(function (checkBox) {
        if (checkBox.checked === false) {
            notChecked += 1;
        }
    })

    //if all unchecked return false, else return true
    if (notChecked === array.length) {
        return false;
    } else {
        return true;
    }
}

//make sure at least one category is checked
async function checkCategories() {
    let category = isChecked(categoryCheckBoxes);
    //save choice if checkbox checked else display alert
    if (category) {
        saveChoices(categoryCheckBoxes);
        return true;
    } else {
        // ERROR HANDLING
        return false;
    }
}


//create dictionary containing each setting checkbox and their state
function createDictionary() {
    let dict = {};
    [].forEach.call(checkBoxes, function (checkBox) {
        dict[checkBox.id] = checkBox.checked;
    })
    return (dict);
}

//send setting checkbox states to python
async function sendChoices() {
    let dict = createDictionary();
    let json_dict = JSON.stringify(dict);
    console.log(json_dict)
    //might need to add more in body + error handling
    $.post("/selection", {
        javascript_data: json_dict
    });
}

//send user suggestion to python fix radio buttons
function sendSuggestion() {
    let deaths = document.getElementById('s_deaths');
    let roll = document.getElementById('s_roll');
    let description = document.getElementById('s_description');
    let eventName = document.getElementById('s_eventName');
    let email = document.getElementById('s_email');
    let categories = document.getElementsByName('categories');
    let category = "";
    //set category to selected radio button
    [].forEach.call(categories, function (radioButton) {
        if (radioButton.checked) {
            category = radioButton.id
        }
    });

    //create dictionary with all values
    let dict = {
        'death': deaths.checked,
        'roll': roll.checked,
        'description': description.value,
        'eventName': eventName.value,
        'category': category,
        'email': email.value
    };

    //change to json object then send to python

    let json_dict = JSON.stringify(dict);

    $.post("/suggest", {
        javascript_data: json_dict,
    }
        , (status) => {
            suggestionSuccess(status)

        });

}


function suggestionSuccess(status) {
    if (status == 'Ok') {
        $("#suggestSuccess").fadeIn(300).delay(2000).fadeOut(400);
    } else {
        $("#suggestFailure").fadeIn(300).delay(2000).fadeOut(400);
    }
}

//when 'all' button is pressed, check all respective checkboxes
function checkAll(id) {
    if (id == "allCategories") {
        categoryCheckBoxes.forEach(function (checkbox) {
            checkbox.checked = true;
        })
    } else if (id == "allPacks") {
        packCheckBoxes.forEach(function (checkbox) {
            checkbox.checked = true;
        })
    }
}


//save button functionality
async function save() {
    //save user choice for packs included
    saveChoices(packCheckBoxes);

    //see if at least one category has been checked and save if it has been
    let saved = await checkCategories();
    let deathIncluded = document.getElementById('deaths');
    console.log(saved);
    //set whether save is valid or not for generate button
    localStorage.setItem('saveValid', String(saved))

    //if categories are good
    if (saved) {
        $("#saveSuccess").fadeIn(300).delay(1000).fadeOut(400);
        console.log('saved');
        //save deathIncluded state and show confirmation
        localStorage.setItem(deathIncluded.id, deathIncluded.checked);
    } else {
        console.log('bad');
        $("#saveFailure").fadeIn(300).delay(1000).fadeOut(400);

    }

}

//called when generate new event button clicked
async function generate() {
    //if valid settings generate new event else show failure notification

    if (JSON.parse(localStorage.getItem('saveValid')) === true) {
        await sendChoices();
        location.assign('/generate');
    } else {
        $("#generateFailure").fadeIn(300).delay(1000).fadeOut(400);
    }
}

//random number generator for events that need it
function random() {
    document.getElementById('randomBtn').classList.toggle("down");
    let num = Math.random() * 11 | 0;
    document.getElementById("randomNum").innerHTML = String(num);

}


