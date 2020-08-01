var packCheckBoxes = document.getElementsByName("packsIncluded[]");
var categoryCheckBoxes = document.getElementsByName("categoriesIncluded[]");
var checkBoxes = document.getElementsByClassName("checkBox")


function save(array) {
    array.forEach(function (checkBox) {
                localStorage.setItem(checkBox.id, checkBox.checked);

    })
}

//make sure at least one category is checked
function checkCategories() {
    let category = isChecked(categoryCheckBoxes);
    if (category) {
            save(categoryCheckBoxes);
            return true
        } else {
            alert("Please select one or more categories")
        }
}

function checkAll(id) {
    if (id == "allCategories") {
        categoryCheckBoxes.forEach(function (checkbox) {
            checkbox.checked = true;
        })
    }

    else if (id == "allPacks") {
        packCheckBoxes.forEach(function (checkbox) {
            checkbox.checked = true;
        })
    }
}
function isChecked(array) {
    let notChecked = 0
    array.forEach(function (checkBox) {
        if (checkBox.checked == false) {
            notChecked += 1;
        }
    })

    //all unchecked
    if (notChecked == array.length) {
        //alert("you must select a category");
        return false;
    } else {
        //save()
        return true
    }
}

//load whether checkboxes where checked or unchecked
function load() {
    [].forEach.call(checkBoxes, function (checkBox) {
        let checked = JSON.parse(localStorage.getItem(checkBox.id));
        document.getElementById(checkBox.id).checked = checked;
    });
}


//create dictonary of each ch3ckbox and their state
function createDictonary() {
    let dict = {};
    [].forEach.call(checkBoxes, function (checkBox) {
        dict[checkBox.id] = checkBox.checked;
    })
    return (dict);
}

function sendChoices() {
    let dict = createDictonary();
    let json_dict = JSON.stringify(dict);
    //might need to add more in body + error handling
    $.post("/selection", {
        javascript_data: json_dict
    });
}


function generate() {
    save(packCheckBoxes)
    let saved = checkCategories();
    let deathIncluded = document.getElementById('deaths')
    if (saved){
        localStorage.setItem(deathIncluded.id, deathIncluded.checked);
        sendChoices();
        location.assign('/generate')
    }
}

