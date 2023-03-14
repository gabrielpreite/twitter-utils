// GENERAL FUNCTIONS
function validazione() {
    // sostituisce i caratteri speciali con spazi
    let str = document.getElementById("query").value;
    const newStr = str.replace(/[^A-Za-zÀ-ÖØ-öø-ÿ0-9@_]/g, " ");
    document.getElementById("query").value = newStr;

    // ripulire whitespace iniziali e finali
    str = document.getElementById("query").value;
    str = str.trim();
    document.getElementById("query").value = str;
    // la query puo' essere vuota solo se facciamo ricerca per location
    if (str == "" && !(document.getElementById("location").selected)) {
        alert("la query non puo' contenere solo spazi o essere vuota");
        return false;
    }

    // lunghezza username <16
    if (document.getElementById("username").selected) {
        if (document.getElementById("query").value.length > 15) {
            alert("username deve essere minore di 16 caratteri")
            return false;
        }
    }

    // keyword <128
    if (document.getElementById("keyword").selected) {
        if (document.getElementById("query").value.length > 127) {
            alert("la keyword deve essere minore di 128 caratteri")
            return false;
        }
    }

    const date = new Date();
    // validiamo le date
    let data_inizio = document.getElementById("data_inizio").value;
    let data_fine = document.getElementById("data_fine").value;
    let data_oggi = "" + String(date.getFullYear()).padStart(4, '0') + "-" + String(date.getMonth() + 1).padStart(2, '0') + "-" + String(date.getDate()).padStart(2, '0');

    // la data di inizio deve essere <= della data di fine
    if (data_inizio > data_fine) {
        alert("la data di inizio deve essere <= della data di fine")
        return false;
    }
    // la data di fine deve essere <= della data di oggi
    if (data_fine > data_oggi) {
        alert("la data di fine deve essere <= della data di oggi")
        return false;
    }
    // la data di inizio deve essere >= 2006-03-21
    if (data_inizio < "2006-03-21") {
        alert("la data di inizio deve essere dopo la data di creazione di Twitter (21-03-2006)")
        return false;
    }
    return true;
}

function updateRange() {
    let num = document.getElementById("tweets-number");
    let val = document.getElementById("tweets-range").value;
    if (val == 1) {
        num.innerHTML = "Mostra " + val + " tweet";
    } else {
        num.innerHTML = "Mostra " + val + " tweets";
    }
}

function updateChessRange() {
    let num = document.getElementById("move_number");
    let val = document.getElementById("move_time").value;
    if (val == 1) {
        num.innerHTML = "Turno di " + val + " ora";
    } else {
        num.innerHTML = "Turno di " + val + " ore";
    }
}

function setDate() {
    const date = new Date();

    // default da oggi
    let data_fine = "" + String(date.getFullYear()).padStart(4, '0') + "-" + String(date.getMonth() + 1).padStart(2, '0') + "-" + String(date.getDate()).padStart(2, '0')

    // a 7 giorni fa
    let differenza = (24 * 60 * 60 * 1000) * 7;
    date.setTime(date.getTime() - differenza);

    let data_inizio = "" + String(date.getFullYear()).padStart(4, '0') + "-" + String(date.getMonth() + 1).padStart(2, '0') + "-" + String(date.getDate()).padStart(2, '0')

    document.getElementById("data_inizio").value = data_inizio;
    document.getElementById("data_fine").value = data_fine;
}

// HELPERS
// verifica se un elemento si e' nella visualizzazione corrente
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// ONLOAD
document.onload = $("#location-tab").hide();
setDate(); // setto le date di default
