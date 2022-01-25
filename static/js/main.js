
function updateTextInput(vals) {
    document.getElementById('priceRange').innerHTML = vals;
}

function decreasePrice() {
    var price = document.getElementById('range').value;
    document.getElementById('range').value = String(parseInt(price) - parseInt(1));
    document.getElementById('priceRange').innerHTML = String(parseInt(price) - parseInt(1));
}

function increasePrice() {
    var price = document.getElementById('range').value;
    document.getElementById('range').value = String(parseInt(price) + parseInt(1));
    document.getElementById('priceRange').innerHTML = String(parseInt(price) + parseInt(1));

}

