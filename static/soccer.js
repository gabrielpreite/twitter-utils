function parseDate(datetime) {
    let day = datetime.getDate()
    let month = datetime.getMonth() + 1
    let year = datetime.getFullYear()
    return day + "/" + month + "/" + year
}

function printMatches(partite) {
    try {
        let el = document.getElementById("matches-body")

        for (let match of partite["response"]) {

            let row = document.createElement("tr")

            // data
            // conversione ISO date -> date time format
            const datetime = new Date(match["fixture"]["date"])

            let date = document.createElement("td")
            date.setAttribute("class", "date-cell")
            date.innerHTML = parseDate(datetime)
            row.appendChild(date)


            // home team
            let home_td = document.createElement("td")
            home_td.setAttribute("class", "home_td")

            let home_img = document.createElement("img")
            home_img.src = match["teams"]["home"]["logo"]
            home_img.style.height = "30px"

            let home = document.createElement("span")
            home.innerHTML = match["teams"]["home"]["name"] + " "
            home_td.appendChild(home)
            home_td.appendChild(home_img)

            row.appendChild(home_td)

            // score
            let score = document.createElement("td")
            score.setAttribute("class", "score-td")
            if ((match["goals"]["home"] == null) || (match["goals"]["away"] == null)) {
                score.innerHTML = "TBD"
            } else {
                score.innerHTML = match["goals"]["home"] + " - " + match["goals"]["away"]
            }

            row.appendChild(score)

            // guest team
            let guest_td = document.createElement("td")
            guest_td.setAttribute("class", "guest_td")


            let guest_img = document.createElement("img")
            guest_img.src = match["teams"]["away"]["logo"]
            guest_img.style.height = "30px"
            guest_td.appendChild(guest_img)

            let guest = document.createElement("span")
            guest.innerHTML = " " + match["teams"]["away"]["name"]
            guest_td.appendChild(guest)

            row.appendChild(guest_td)

            let button_td = document.createElement("td")
            button_td.setAttribute("class", "button-td")

            let button = document.createElement("input")
            button.type = "submit"
            button.value = "apri"
            button.setAttribute("class", "btn btn-outline-secondary")

            let form = document.createElement("form")
            form.action = "/soccer"
            form.method = "POST"
            form.style = "text-align: center;"

            let input = document.createElement("input")
            input.value = match["fixture"]["id"]
            input.style = "display: none;"
            input.type = "text"
            input.name = "id"

            form.append(button)
            form.append(input)

            button_td.appendChild(form)

            row.appendChild(button_td)

            el.appendChild(row)
        }
    } catch {
        return false
    } return true
}

function printStats(dettagli) {
    let tiri_porta_home = dettagli["response"][0]["statistics"][0]["statistics"][0]["value"]
    let tiri_porta_guest = dettagli["response"][0]["statistics"][1]["statistics"][0]["value"]
    document.getElementById("tiri-porta-home").style.width = percentuale(tiri_porta_home, tiri_porta_guest)[0]
    document.getElementById("tiri-porta-guest").style.width = percentuale(tiri_porta_home, tiri_porta_guest)[1]
    document.getElementById("tiri-porta-start").innerHTML = tiri_porta_home
    document.getElementById("tiri-porta").innerHTML = "Tiri in Porta"
    document.getElementById("tiri-porta-end").innerHTML = tiri_porta_guest

    let tiri_totali_home = dettagli["response"][0]["statistics"][0]["statistics"][2]["value"]
    let tiri_totali_guest = dettagli["response"][0]["statistics"][1]["statistics"][2]["value"]
    document.getElementById("tiri-totali-home").style.width = percentuale(tiri_totali_home, tiri_totali_guest)[0]
    document.getElementById("tiri-totali-guest").style.width = percentuale(tiri_totali_home, tiri_totali_guest)[1]
    document.getElementById("tiri-totali-start").innerHTML = tiri_totali_home
    document.getElementById("tiri-totali").innerHTML = "Tiri Totali"
    document.getElementById("tiri-totali-end").innerHTML = tiri_totali_guest


    let falli_home = dettagli["response"][0]["statistics"][0]["statistics"][6]["value"]
    let falli_guest = dettagli["response"][0]["statistics"][1]["statistics"][6]["value"]
    document.getElementById("falli-home").style.width = percentuale(falli_home, falli_guest)[0]
    document.getElementById("falli-guest").style.width = percentuale(falli_home, falli_guest)[1]
    document.getElementById("falli-start").innerHTML = falli_home
    document.getElementById("falli").innerHTML = "Falli"
    document.getElementById("falli-end").innerHTML = falli_guest

    let angolo_home = dettagli["response"][0]["statistics"][0]["statistics"][7]["value"]
    let angolo_guest = dettagli["response"][0]["statistics"][1]["statistics"][7]["value"]
    document.getElementById("angolo-home").style.width = percentuale(angolo_home, angolo_guest)[0]
    document.getElementById("angolo-guest").style.width = percentuale(angolo_home, angolo_guest)[1]
    document.getElementById("angolo-start").innerHTML = angolo_home
    document.getElementById("angolo").innerHTML = "Calci d'Angolo"
    document.getElementById("angolo-end").innerHTML = angolo_guest

    let fuorigioco_home = dettagli["response"][0]["statistics"][0]["statistics"][8]["value"]
    let fuorigioco_guest = dettagli["response"][0]["statistics"][1]["statistics"][8]["value"]
    document.getElementById("fuorigioco-home").style.width = percentuale(fuorigioco_home, fuorigioco_guest)[0]
    document.getElementById("fuorigioco-guest").style.width = percentuale(fuorigioco_home, fuorigioco_guest)[1]
    document.getElementById("fuorigioco-start").innerHTML = fuorigioco_home
    document.getElementById("fuorigioco").innerHTML = "Fuorigioco"
    document.getElementById("fuorigioco-end").innerHTML = fuorigioco_guest

    let possesso_home = dettagli["response"][0]["statistics"][0]["statistics"][9]["value"]
    let possesso_guest = dettagli["response"][0]["statistics"][1]["statistics"][9]["value"]
    document.getElementById("possesso-home").style.width = possesso_home
    document.getElementById("possesso-guest").style.width = possesso_guest
    document.getElementById("possesso-start").innerHTML = possesso_home
    document.getElementById("possesso").innerHTML = "Possesso Palla "
    document.getElementById("possesso-end").innerHTML = possesso_guest

    let parate_home = dettagli["response"][0]["statistics"][0]["statistics"][8]["value"]
    let parate_guest = dettagli["response"][0]["statistics"][1]["statistics"][8]["value"]
    document.getElementById("parate-home").style.width = percentuale(parate_home, parate_guest)[0]
    document.getElementById("parate-guest").style.width = percentuale(parate_home, parate_guest)[1]
    document.getElementById("parate-start").innerHTML = parate_home
    document.getElementById("parate").innerHTML = "Parate"
    document.getElementById("parate-end").innerHTML = parate_guest
}

function percentuale(a, b) {
    if (a == 'null') { a = 0 }
    if (b == 'null') { b = 0 }

    let c = parseFloat(a + b)

    if (c != 0) {
        return [`${a / c * 100}%`, `${b / c * 100}%`]
    } else { return ["0%", "0%"] }
}

function printTeams(dettagli) {
    document.getElementById("home-name").innerHTML = dettagli["response"][0]["teams"]["home"]["name"]
    document.getElementById("home-logo").src = dettagli["response"][0]["teams"]["home"]["logo"]
    document.getElementById("guest-name").innerHTML = dettagli["response"][0]["teams"]["away"]["name"]
    document.getElementById("guest-logo").src = dettagli["response"][0]["teams"]["away"]["logo"]
}

function printLineups(dettagli) {
    try {

        let dict = {
            "G": "Portiere",
            "D": "Difensore",
            "M": "Centrocampista",
            "F": "Attaccante"
        }

        let el_home = document.getElementById("starters-home")
        for (let giocatore of dettagli["response"][0]["lineups"][0]["startXI"]) {
            let row = document.createElement("tr")
            let playerName = document.createElement("td")
            playerName.innerHTML = giocatore["player"]["name"]
            row.appendChild(playerName)

            let role = document.createElement("td")
            role.innerHTML = dict[giocatore["player"]["pos"]]
            row.appendChild(role)

            el_home.appendChild(row)
        }

        let el_guest = document.getElementById("starters-guest")
        for (let giocatore of dettagli["response"][0]["lineups"][1]["startXI"]) {
            let row = document.createElement("tr")
            let playerName = document.createElement("td")
            playerName.innerHTML = giocatore["player"]["name"]
            row.appendChild(playerName)

            let role = document.createElement("td")
            role.innerHTML = dict[giocatore["player"]["pos"]]
            row.appendChild(role)

            el_guest.appendChild(row)
        }
    } catch {
        return false
    } return true
}

function printScore(dettagli) {
    document.getElementById("score").innerHTML = dettagli["response"][0]["goals"]["home"] + " - " + dettagli["response"][0]["goals"]["away"]
}

// da finire
function printEvents(dettagli) {
    try {
        let el_home = document.getElementById("ehome-body")
        let el_guest = document.getElementById("eguest-body")

        for (let evento of dettagli["response"][0]["events"]) {
            let row = document.createElement("tr")

            let minute = document.createElement("td")
            minute.innerHTML = evento["time"]["elapsed"] + "\'"
            if (evento["time"]["extra"] != null) {
                minute.innerHTML += "+" + evento["time"]["extra"] + "\'"
            }


            let e = document.createElement("td")

            if (evento["type"] == "Card") {
                e.innerHTML = (evento["detail"] == "Yellow Card" ? '<span style="background-color: yellow; font-weight: bold;">A</span>'
                    : '<span style="background-color: red; font-weight: bold;">Es</span>') + " " + evento["player"]["name"]
            } else if (evento["type"] == "subst") {
                e.innerHTML = '<i class="fa-solid fa-arrow-up" style="color: green"></i>' + evento["assist"]["name"] + " - " + '<i class="fa-solid fa-arrow-down" style="color: red"></i>' + evento["player"]["name"]
            } else if (evento["type"] == "Goal") {
                e.innerHTML = '<div class="fw-bold"><i class="fa-regular fa-futbol"></i> ' + evento["player"]["name"] + "</div>"
            } else continue


            if (evento["team"]["name"] == dettagli["response"][0]["teams"]["home"]["name"]) {
                e.setAttribute("class", "text-start")
                minute.setAttribute("class", "text-start")
                row.appendChild(minute)
                row.appendChild(e)
                el_home.appendChild(row)
            } else {
                e.setAttribute("class", "text-end")
                minute.setAttribute("class", "text-end")
                row.appendChild(e)
                row.appendChild(minute)
                el_guest.append(row)
            }
        }
    } catch {
        return false
    } return true
}

function printTweets(results) {
    try {
        let el_tweets = document.getElementById("tweets")

        if (results["meta"]["result_count"] > 0) {
            for (let tweet of results["data"]) {
                // creazione colonna
                let col = document.createElement("div")
                col.setAttribute("class", "col-4 align-content-middle")

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

                // creazione e riempimento date
                let date = document.createElement("span")
                date.className = "created_at fw-light"
                date.innerHTML = "twittato il " + parseDate(datetime) + " alle " + datetime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                cardBody.appendChild(date)

                newDiv.appendChild(cardBody)
                col.append(newDiv)
                el_tweets.appendChild(col)
            }
        }
    } catch {
        return false
    } return true
}

function printImages(results) {
    try {
        let photos = document.getElementById("tweet-pics")

        if (results["meta"]["result_count"] > 0) {
            for (let tweet of results["data"]) {
                // creazione e riempimento media
                if (tweet.hasOwnProperty("attachments")) {
                    let pic_col = document.createElement("div")
                    pic_col.setAttribute("class", "col")

                    let media = document.createElement("img")
                    media.src = tweet["attachments"]["media"]["url"] != "" ? tweet["attachments"]["media"]["url"] : tweet["attachments"]["media"]["preview_url"]
                    media.alt = "media"
                    media.setAttribute("class", "media")
                    media.setAttribute("style", "height: 200px; border-bottom; 2rem;")
                    pic_col.appendChild(media)
                    photos.appendChild(pic_col)
                }
            }

        }
    } catch {
        return false
    } return true
}

function tweetsScroll() {
    document.getElementById("tweets").scrollBy(1, 0);
    setTimeout(tweetsScroll, 30);
}

function picsScroll() {
    document.getElementById("tweet-pics").scrollBy(1, 0);
    setTimeout(picsScroll, 30);
}

// funzione generale
function printMatch(dettagli) {
    printScore(dettagli)
    printTeams(dettagli)
    printStats(dettagli)
    printLineups(dettagli)
    printEvents(dettagli)
}

module.exports = printMatches;
module.exports = printStats;
module.exports = printTeams;
module.exports = printLineups;
module.exports = printScore;
module.exports = printEvents;
module.exports = printTweets;
module.exports = printImages;
module.exports = printMatch;

module.exports = percentuale;