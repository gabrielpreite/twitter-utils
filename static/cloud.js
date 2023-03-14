function cloud() {
    //Creazione e parametri termcloud
    let color = d3.scale.category20()

    d3.layout.cloud()
        .size([800, 500])
        .words(frequency_list)
        .padding(2)
        .fontSize(function (d) { return d.size })
        .on("end", draw)
        .start();

    function draw(words) {
        d3.select("#nuvola").append("svg")
            .attr("width", 800)
            .attr("height", 500)
            .attr("id", "cloud")
            .append("g")
            .attr("transform", "translate(" + 800 / 2 + "," + 500 / 2 + ")")
            .selectAll("text")
            .data(words)
            .enter().append("text")
            .style("font-size", function (d) { return d.size + "px"; })
            .style("fill", function (d, i) { return color(i); })
            .attr("text-anchor", "middle")
            .attr("transform", function (d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .text(function (d) { return d.text; });
    }
    $("#nuvola").hide();

}

function toggleCloud() {
    $("#nuvola").toggle();
    $("#timeline").hide();
    $("#statistiche").hide();
    $(".bollino").hide();
}

function highlight() { // Cloud Interattiva
    let listaTesti = document.getElementsByClassName("tweet-text");
    let cloud = document.querySelector('#nuvola');

    // onclick su una parola della term cloud - evidenzia in tweet
    cloud.addEventListener('click', function (event) {
        let target = event.target;
        let color = event.target.style.fill;
        let count = 0;
        for (let tweetText of listaTesti) {
            let text = tweetText.textContent;
            let regex = new RegExp('(' + target.textContent + ')', 'ig');
            text = text.replace(regex, `<span style="color: ${color}; font-size: large; font-weight: 600">$1</span>`);
            if (regex.test(text)) { count++ }
            tweetText.innerHTML = text;
        }

        // rimuovi p con counter precedente se esistente
        let r = document.getElementById("cloud-times")
        if (r != null) {
            r.parentNode.removeChild(r);
        }

        // aggiungi p con counter parole
        if (target.textContent.length < 30) {
            let cloudTimes = document.createElement("p")
            cloudTimes.setAttribute("id", "cloud-times")
            cloudTimes.innerHTML = `La parola <span style="background-color: ${color}; font-size: large; font-weight: 600">${target.textContent}</span> e' stata tweettata <u style="font-size: large; font-weight: 500;">${count}</u> volte!`
            cloud.appendChild(cloudTimes)
        }
    }, false);
}