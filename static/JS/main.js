var packCheckBoxes = document.getElementsByName("packsIncluded[]");
var categoryCheckBoxes = document.getElementsByName("categoriesIncluded[]");
var checkBoxes = document.getElementsByClassName("checkBox")


function save(array) {
    array.forEach(function (checkBox) {
                localStorage.setItem(checkBox.id, checkBox.checked);

    })



    //  packCheckBoxes.forEach(function (checkBox) {
    //      localStorage.setItem(checkBox.id, checkBox.checked);
    //  });
}

//make sure at least one category is checked
function checkCategories() {
    var pack = isChecked(packCheckBoxes);
    if (pack) {
        save(packCheckBoxes)
        var category = isChecked(categoryCheckBoxes);
        if (category) {
            save(categoryCheckBoxes);
        } else {
            alert("please select a category")
        }
    } else {
        alert("please select a pack")
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
    if (notChecked == categoryCheckBoxes.length) {
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

//if basegame only checked uncheck other packs and vice-versa
function setBasegameOnlyState(element) {
    if ((element.id != "basegame") && (element.checked)) {
        document.getElementById('basegame').checked = false;
    } else if (element.id == "basegame" && element.checked) {
        packCheckBoxes.forEach(function (checkBox) {
            //don't uncheck basegame
            if (checkBox.id != "basegame") {
                document.getElementById(checkBox.id).checked = false;
            }
        })
    }
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
    json_dict = JSON.stringify(dict);
    //might need to add more in body + error handling
    $.post("/selection", {
        javascript_data: json_dict
    });

    $.get("/generate");
    // $.ajax({
    //         type: 'POST',
    //         url: "img/test.py",
    //         success: function () {
    //             alert("working")
    //         },
    //         error: function () {
    //             alert("Not Working")
    //         }
    //     });
}

