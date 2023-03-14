let x = results["meta"]["grafico_barre"]["x"];
let y = results["meta"]["grafico_barre"]["y"];

let dataTL =
    [{
        y: y,
        x: x,
        type: "scatter"
    }]

let layoutTL = {
    height: 400,
    width: 500,
    bargap: 0.05,
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)'
};

function toggleTimeline() {
    $("#timeline").toggle();
    $("#nuvola").hide();
    $("#statistiche").hide();
    $(".bollino").hide();
}