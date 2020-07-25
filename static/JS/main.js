var packCheckBoxes = document.getElementsByName("packsIncluded[]");

//send whether deaths are wanted
function checkCheckBox() {
    createDictonary();
    let checkBox = document.getElementById('deaths');
    document.getElementById('deathStorage').value = checkBox.checked;
}

function save() {
    packCheckBoxes.forEach(function (checkBox) {
        localStorage.setItem(checkBox.id, checkBox.checked);
    });
}

function load() {
    packCheckBoxes.forEach(function (checkBox) {
        let checked = JSON.parse(localStorage.getItem(checkBox.id));
        document.getElementById(checkBox.id).checked = checked;
    })

}

//if basegame only checked uncheck other packs and vice-versa
function setBasegameOnlyState(element) {
    if ((element.id != "basegame") && (element.checked)) {
        document.getElementById('basegame').checked = false;
    } else if (element.checked) {
        packCheckBoxes.forEach(function (checkBox) {
            document.getElementById(checkBox.id).checked = false;
        })
    }
}


//create dictonary of cehckbox and their state
function createDictonary() {
    let dict = {};
    packCheckBoxes.forEach(function (checkBox) {
        dict[checkBox.id] = checkBox.checked;
    })


}


