var packCheckBoxes = document.getElementsByName("packsIncluded[]");
var categoryCheckBoxes = document.getElementsByName("categoriesIncluded[]");
var checkBoxes = document.getElementsByClassName("checkBox")
var saveBtn = document.getElementById('saveBtn')


//save whether checkbox is checked or not in local storage
function saveChoices(array) {
    array.forEach(function (checkBox) {
        localStorage.setItem(checkBox.id, checkBox.checked);

    })
}

//load whether checkboxes where checked or unchecked
function load() {
    [].forEach.call(checkBoxes, function (checkBox) {
        let checked = JSON.parse(localStorage.getItem(checkBox.id));
        document.getElementById(checkBox.id).checked = checked;
    });
}

//check whether a checkbox in the group has been selected
function isChecked(array) {
    let notChecked = 0
    array.forEach(function (checkBox) {
        if (checkBox.checked == false) {
            notChecked += 1;
        }
    })

    //all unchecked
    if (notChecked == array.length) {
        return false;
    } else {
        return true
    }
}

//make sure at least one category is checked
function checkCategories() {
    let category = isChecked(categoryCheckBoxes);
    //save choice if checkbox checked else display alert
    if (category) {
        saveChoices(categoryCheckBoxes);
        return true;
    } else {
        $("#saveFailure").fadeIn(300).delay(1000).fadeOut(400);
        return false;
    }
}


//create dictonary of each checkbox and their state
function createDictonary() {
    let dict = {};
    [].forEach.call(checkBoxes, function (checkBox) {
        dict[checkBox.id] = checkBox.checked;
    })
    return (dict);
}

//send checkbox states to python
function sendChoices() {
    let dict = createDictonary();
    let json_dict = JSON.stringify(dict);
    //might need to add more in body + error handling
    $.post("/selection", {
        javascript_data: json_dict
    });
}

function sendSuggestion() {
    deaths = document.getElementById('s_deaths');
    roll = document.getElementById('s_roll');
    let description = document.getElementById('s_description');
    eventName = document.getElementById('s_eventName');
    categories = document.getElementsByName('categories')
    let category = "";
    [].forEach.call(categories, function (checkBox) {
        if (checkBox.checked) {
            category = checkBox.id
        }
    });

    let dict = {
        'death': deaths.checked,
        'roll': roll.checked,
        'description': description.value,
        'eventName': eventName.value,
        'category': category
    };


    let json_dict = JSON.stringify(dict);

    $.post("/suggest", {
        javascript_data: json_dict,
        success: function (msg) {
            $("#suggestSuccess").fadeIn(300).delay(1000).fadeOut(400);
        },
        error: function (error) {
            $("#suggestFailure").fadeIn(300).delay(1000).fadeOut(400);
        }
    });
}


//when 'all' button is pressed, checked all respective checboxes
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
function save() {
    //save user choice for packs included
    saveChoices(packCheckBoxes)
    //see if at least one category has been checked and save if it has been
    let saved = checkCategories();
    let deathIncluded = document.getElementById('deaths')
    localStorage.setItem('saveValid', saved)

    //if categories are good
    if (saved) {
        //save deathIncluded state
        localStorage.setItem(deathIncluded.id, deathIncluded.checked);
        $("div.success").fadeIn(300).delay(1000).fadeOut(400);
    }

}

function generate() {
    if (JSON.parse(localStorage.getItem('saveValid')) === true) {
        sendChoices();
        location.assign('/generate');
    } else {
        $("#generateFailure").fadeIn(300).delay(1000).fadeOut(400);
    }
}

function random() {
    document.getElementById('randomBtn').classList.toggle("down");
    num = Math.random() * 11 | 0;
    document.getElementById("randomNum").innerHTML = num;

}
