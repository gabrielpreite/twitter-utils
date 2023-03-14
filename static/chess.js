function printTweet(tweet, color) {
    // creazione contenitore card tweet
    let newDiv = document.createElement("div")
    newDiv.setAttribute("class", "card m-3")

    // creazione e riempimento card body
    let cardBody = document.createElement("div")
    cardBody.setAttribute("class", "card-body")

    // creazione e riempimento propic
    let propic = document.createElement("img")
    propic.src = tweet["profile_image_url"]
    propic.alt = "profile picture"
    propic.setAttribute("class", "propic float-start")

    // creazione e riempimento nome
    let nome = document.createElement("h6")
    nome.setAttribute("class", "name card-title fw-bold mb-0")
    nome.innerHTML = tweet["name"]
    cardBody.append(propic)
    cardBody.appendChild(nome)

    // creazione e riempimento username
    let username = document.createElement("h7")
    username.setAttribute("class", "username card-subtitle fw-light")
    username.innerHTML = "@" + tweet["username"]
    cardBody.appendChild(username)

    // creazione e riempimento tweet text
    let text = document.createElement("p")
    text.setAttribute("class", "tweet-text card-text pt-2")
    text.innerHTML = tweet["text"]
    cardBody.appendChild(text)

    // conversione ISO date -> date time format
    const datetime = new Date(tweet["created_at"])

    function parseDate(datetime) {
        let day = datetime.getDate()
        let month = datetime.getMonth() + 1
        let year = datetime.getFullYear()
        return day + "/" + month + "/" + year
    }

    // creazione e riempimento date
    let date = document.createElement("span")
    date.className = "created_at fw-light"
    date.innerHTML = "twittato il " + parseDate(datetime) + " alle " + datetime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    cardBody.appendChild(date)

    newDiv.appendChild(cardBody)
    document.getElementById(color + "-tweets").appendChild(newDiv)
}

function getTimeLeft(startDate, move_time) {
    startDate = new Date(startDate * 1000)
    let countDownDate = new Date(startDate.getTime() + move_time * 60 * 60000)
    let distance = countDownDate - new Date().getTime()
    if (distance < 0) {
        distance = -distance
    }
    if (distance < 60 *60000){
        distance+=20000 // aggiunta delay
    } 
    return distance
}

function setTimer(startDate, move_time, color) {
    startDate = new Date(startDate * 1000)
    let countDownDate = new Date(startDate.getTime() + move_time * 60 * 60000)

    // Update the count down every 1 second
    let x = setInterval(function () {

        // Get today's date and time
        let now = new Date().getTime();

        // Find the distance between now and the count down date
        let distance = countDownDate - now;

        // Time calculations for days, hours, minutes and seconds
        let days = Math.floor(distance / (1000 * 60 * 60 * 24));
        let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        let seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Display the result in the element with id="demo"
        document.getElementById(color + "-timer").innerHTML = '<em class="fa-solid fa-clock"></em> ' + days + "d " + hours + "h " + minutes + "m " + seconds + "s ";

        // If the count down is finished, write some text
        if (distance < 0) {
            clearInterval(x);
            document.getElementById(color + "-timer").innerHTML = '<em class="fa-solid fa-clock"></em>' + " EXPIRED"
        }

        if (color == "white") {
            document.getElementById("black-timer").innerHTML = '<em class="fa-solid fa-clock"></em>' + " IN ATTESA"
        } else {
            document.getElementById("white-timer").innerHTML = '<em class="fa-solid fa-clock"></em>' + " IN ATTESA"
        }
    }, 1000);
}

function scoreUpdate(white, black) {
    document.getElementById("white-score") = white
    document.getElementById("black-score") = black
}

function validazioneUser() {
    // guarda che non ci siano caratteri non ammessi
    let str = document.getElementById("query").value;
    const regex = new RegExp(/^@?(\w){1,15}$/);
    if (!regex.test(str)) {
        alert("la ricerca non puo' contenere solo spazi o essere vuota, lo username deve essere minore di 16 caratteri")
        return false;
    }


    // ripulire whitespace iniziali e finali
    str = document.getElementById("query").value;
    str = str.trim();
    document.getElementById("query").value = str;

    // la query non puo' essere vuota
    if (str == "") {
        alert("la query non puo' contenere solo spazi o essere vuota");
        return false;
    }

    // lunghezza username <16
    if (document.getElementById("query").value.length > 15) {
        alert("username deve essere minore di 16 caratteri")
        return false;
    }
    return true;
}