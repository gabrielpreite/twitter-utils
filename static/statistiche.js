let dataSTAT = [{
    values: [results["meta"]["grafico_sentiment"]["values"][0], results["meta"]["grafico_sentiment"]["values"][2], results["meta"]["grafico_sentiment"]["values"][1]],
    labels: ['Positive', 'Neutral', 'Negative'],
    type: 'pie',
    marker: { colors: ['rgb(34, 139, 34)', 'rgb(0, 71, 171)', 'rgb(238, 75, 43)'] }
}];

let layoutSTAT = {
    height: 400,
    width: 500,
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)'
};

function toggleStats() {
    $("#statistiche").toggle();
    $(".bollino").toggle();
    $("#nuvola").hide();
    $("#timeline").hide();
}