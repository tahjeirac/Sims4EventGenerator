function checkCheckBox() {
    var checkBox = document.getElementById('deaths');
    document.getElementById('deathStorage').value = checkBox.checked;
    save(checkBox);
}

function save(checkBox) {
    localStorage.setItem("checkbox1", checkBox.checked);

}

function load(){
    var checked = JSON.parse(localStorage.getItem('checkbox1'));
    document.getElementById("deaths").checked = checked;
}

