// MAP SETUP
// definisce nuova icona -- RED ICON -- libreria github https://github.com/pointhi/leaflet-color-markers
const redIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});
// definisce nuova icona -- BLUE ICON -- libreria github https://github.com/pointhi/leaflet-color-markers
const blueIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

// MAP METHODS
function showMap() {
    $("#location-tab").slideDown();
}

function hideMap() {
    $("#location-tab").slideUp();
}

function getLat() {
    return document.getElementById("latitudine")
}

function getLong() {
    return document.getElementById("longitudine")
}

// for location
function locationSearch() {
    showMap()
    getLat().removeAttribute("disabled")
    getLong().removeAttribute("disabled")
    document.getElementById("area").className = "col"
    $("#area").show();
}

// for keyword, username, hashtag
function otherSearch() {
    hideMap()
    if (!getLat().hasAttribute("disabled")) {
        getLat().disabled = "false"
        getLong().disabled = "false"
    }
    $("#area").hide()
}
// onclick popup
const popup = L.popup();
function onClickCoord(e) {
    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(map);
    getLat().value = e.latlng.lat
    getLong().value = e.latlng.lng
}

// ONLOAD
document.onload = $("#area").hide()    
