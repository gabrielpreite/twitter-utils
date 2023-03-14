function showTeam(results) {
    let el = document.getElementById("carousel")

    if (results["meta"]["result_count"] > 0) {
        for (let tweet of results["data"]) {
            if ((tweet["attachments"]["media"]["width"] == 1024) && (tweet["attachments"]["media"]["height"] == 512)) {
                let newDiv = document.createElement("div")
                newDiv.setAttribute("class", "carousel-item")

                // creazione e riempimento media
                if (tweet.hasOwnProperty("attachments")) {
                    let media = document.createElement("img")
                    media.src = tweet["attachments"]["media"]["url"]
                    media.alt = "team"
                    newDiv.appendChild(media)
                }

                let user = document.createElement("h5")
                user.setAttribute("class", "carousel-caption d-none d-md-block team-username text-dark fw-bold")
                user.innerHTML = '<div style="color: white;">SQUADRA DI </div>' + "@" + tweet["username"].toUpperCase()
                newDiv.appendChild(user)

                el.appendChild(newDiv)
            }
        }
    }
}

function showLeaderBoard(classifica) {
    try {
        let el = document.getElementById("classifica")

        // inserire nel for il vettore di giocatori
        for (let politico of classifica["politico"]) {

            let newDiv = document.createElement("div")
            newDiv.setAttribute("class", "leaderboard-item")

            // separatore
            let hr = document.createElement("hr")
            hr.setAttribute("style", "border-top: 1.5px solid black;")
            newDiv.appendChild(hr)

            // indicatore di cambiamento posizione (su, giu', non spostato)
            let indicator = document.createElement("span")
            indicator.setAttribute("class", "indicator p-2")

            if (politico["posizione_classifica_old"] > politico["posizione_classifica_new"]) { // salito in classifica
                indicator.innerHTML = '<i class="fa-solid fa-caret-up"></i>'
                indicator.setAttribute("style", "color: green;")
            } else if (politico["posizione_classifica_old"] < politico["posizione_classifica_new"]) {// sceso in classifica 
                indicator.innerHTML = '<i class="fa-solid fa-caret-down"></i>'
                indicator.setAttribute("style", "color: red;")
            } else { // rimasto nella stessa posizione
                indicator.innerHTML = '●'
                indicator.setAttribute("style", "color: blue;")
            }

            newDiv.appendChild(indicator)


            // posizione in classifica
            let posizione = document.createElement("span")
            posizione.setAttribute("class", "position")
            posizione.innerHTML = politico["posizione_classifica_new"]
            newDiv.appendChild(posizione)


            // nome cognome politico
            let nome = document.createElement("span")
            nome.setAttribute("class", "position")
            nome.innerHTML = politico["nome"] + " " + politico["cognome"]
            newDiv.appendChild(nome)

            if (politico["best"] != []) {
                for (let stat of politico["best"]) {
                    if (stat == "worst singlescore") {
                        let badge = document.createElement("span")
                        badge.setAttribute("class", "text-center badge text-bg-danger")
                        badge.innerHTML = stat
                        newDiv.appendChild(badge)
                    } else {
                        let badge = document.createElement("span")
                        badge.setAttribute("class", "text-center badge text-bg-success")
                        badge.innerHTML = stat
                        newDiv.appendChild(badge)
                    }
                }

            }

            // gruppo a destra
            let rightgroup = document.createElement("span")
            rightgroup.setAttribute("class", "right-group")

            // punti 
            let points = document.createElement("span")
            points.setAttribute("class", "points")

            // variabile punti corrisponde a quella che passa dal back i punti
            if (politico["incremento_settimana"] > 0) { // acquisito in classifica
                points.innerHTML = ' (+' + politico["incremento_settimana"] + ')'
            } else if (politico["incremento_settimana"] < 0) {// sceso in classifica 
                points.innerHTML = ' (' + politico["incremento_settimana"] + ')'
            } else {
                points.innerHTML = ' (-)'
            }

            rightgroup.appendChild(points)

            let tot = document.createElement("span")
            tot.setAttribute("class", "punti-tot")
            tot.innerHTML = politico["punteggio"] + "pt."

            rightgroup.appendChild(tot)

            newDiv.appendChild(rightgroup)

            el.appendChild(newDiv)
        }
    } catch {
        return false
    } return true
}

module.exports = showLeaderBoard;