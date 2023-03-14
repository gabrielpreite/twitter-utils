function printSettimana(response) {
    let container = document.getElementById("container")

    let settimana = document.createElement("b")
    settimana.setAttribute("class", "text-center settimana row")
    settimana.innerHTML = "SETTIMANA DAL " + response["data_inizio"] + " AL " + response["data_fine"]

    container.appendChild(settimana)

    for (let puntata of response["puntate"]) {
        let hr = document.createElement("hr")
        container.appendChild(hr)
        let row = document.createElement("div")
        row.setAttribute("class", "row align-items-center")
        row.setAttribute("id", `${puntata["data_puntata"]}`)
        container.appendChild(row)
    }
    printGiorni(response["puntate"])
}

function printGiorni(puntate) {
    for (let giorno of puntate) {
        let row = document.getElementById(`${giorno["data_puntata"]}`)

        let col_date_words = document.createElement("div")
        col_date_words.setAttribute("class", "col container-fluid date-words")

        let date = document.createElement("u")
        date.setAttribute("class", "data row fst-italic")
        date.innerHTML = "Puntata del " + giorno["data_puntata"] + ":"

        let words = document.createElement("div")
        words.setAttribute("class", "row text-center words pt-3")

        for (let parola of giorno["parole"]) {
            let word = document.createElement("div")
            word.setAttribute("class", "parola w-75 text-center b-2 m-1 border border-white")
            word.innerHTML = parola.toUpperCase()
            words.appendChild(word)
        }

        let correct = document.createElement("div")
        correct.setAttribute("class", "correct")
        words.appendChild(correct)

        col_date_words.appendChild(date)
        col_date_words.appendChild(words)
        row.appendChild(col_date_words)

        let col_pie = document.createElement("div")
        col_pie.setAttribute("class", "col torta text-center")
        col_pie.setAttribute("id", `plotly-pie-${giorno["data_puntata"]}`)
        let img_pie = document.createElement("img")
        col_pie.appendChild(img_pie)
        row.appendChild(col_pie)

        // plotly
        let data_pie = [{
            values: [giorno["grafico"]["indovinati"], giorno["grafico"]["totali"] - giorno["grafico"]["indovinati"]],
            labels: ["Corrette", "Sbagliate"],
            type: 'pie',
            marker: { colors: ['rgb(0, 128, 64)', 'rgb(175, 14, 35)'] }
        }];

        let layout_pie = {
            height: 300,
            width: 300,
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)'
        }

        Plotly.newPlot(
            `plotly-pie-${giorno["data_puntata"]}`,
            data_pie,
            layout_pie)

            .then(
                function (gd) {
                    Plotly.toImage(gd, { format: 'png', height: 150, width: 300 })
                        .then(
                            function (url) {
                                img_pie.attr("src", url);
                            }
                        )
                });

        let col_tl = document.createElement("div")
        col_tl.setAttribute("class", "col timeline text-center")
        col_tl.setAttribute("id", `plotly-tl-${giorno["data_puntata"]}`)
        let title_tl = document.createElement("div")
        title_tl.setAttribute("class", "title-tl mb-5 px-0 h5 fw-bold fst-italic")
        title_tl.innerHTML = "Distribuzione dei Vincitori"
        col_tl.appendChild(title_tl)
        let img_tl = document.createElement("img")
        row.appendChild(col_tl)

        let timestamps = []
        let num = []
        let cont = 0

        for (let indovino of giorno["classifica"]) {
            timestamps.push(indovino["time"])
            num.push(cont)
            cont++
        }

        // plotly
        let data_tl = [{
            x: timestamps,
            y: num,
            mode: 'lines',
            type: 'scatter'

        }]

        let layout_tl = {
            height: 300,
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            xaxis: {
                gridcolor: "#d3d3d3",
                gridwidth: 0.3
            },
            yaxis: {
                gridcolor: "#d3d3d3",
                gridwidth: 0.3
            }
        }

        Plotly.newPlot(
            `plotly-tl-${giorno["data_puntata"]}`,
            data_tl,
            layout_tl)

            .then(
                function (gd) {
                    Plotly.toImage(gd, { format: 'png', height: 150, width: 300 })
                        .then(
                            function (url) {
                                img_tl.attr("src", url);
                            }
                        )
                });



        let col_podio = document.createElement("div")
        col_podio.setAttribute("class", "col timeline text-center")

        let first = document.createElement("div")
        first.setAttribute("class", "first")
        first.innerHTML = '🥇'
        for (let persona of giorno["podio"]["primo"]) {
            let p = document.createElement("div")
            p.innerHTML = persona["username"]
            first.appendChild(p)
        }
        col_podio.appendChild(first)

        let second = document.createElement("div")
        second.setAttribute("class", "second")
        second.innerHTML = '🥈'
        for (let persona of giorno["podio"]["secondo"]) {
            let p = document.createElement("div")
            p.innerHTML = persona["username"]
            second.appendChild(p)
        }
        col_podio.appendChild(second)

        let third = document.createElement("div")
        third.setAttribute("class", "third")
        third.innerHTML = '🥉'
        for (let persona of giorno["podio"]["terzo"]) {
            let p = document.createElement("div")
            p.innerHTML = persona["username"]
            third.appendChild(p)
        }
        col_podio.appendChild(third)

        row.appendChild(col_podio)
    }
}

function prevWeek(){
    let data_inizio = new Date(document.getElementsByName("data_inizio")[0].value)
    let data_fine = new Date(document.getElementsByName("data_fine")[0].value)
    data_inizio.setDate(data_inizio.getDate()-7)
    data_fine.setDate(data_fine.getDate()-7)
    document.getElementsByName("data_inizio")[0].value = data_inizio.toISOString().substr(0,10)
    document.getElementsByName("data_fine")[0].value = data_fine.toISOString().substr(0,10)
    document.getElementById("week").submit()
}

function nextWeek() {
    let data_inizio = new Date(document.getElementsByName("data_inizio")[0].value)
    let data_fine = new Date(document.getElementsByName("data_fine")[0].value)
    data_inizio.setDate(data_inizio.getDate() + 7)
    data_fine.setDate(data_fine.getDate() + 7)
    if (data_inizio < (new Date())) {
        document.getElementsByName("data_inizio")[0].value = data_inizio.toISOString().substr(0, 10)
        document.getElementsByName("data_fine")[0].value = data_fine.toISOString().substr(0, 10)
        document.getElementById("week").submit()
    }
}