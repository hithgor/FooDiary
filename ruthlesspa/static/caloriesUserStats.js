const plotContainer = document.getElementById('plotContainer')
const toggleStatsBtn = document.getElementById('toggleStatsBtn')
const wrapLemonContainerBtn = document.getElementById('wrapLemonContainerBtn')


function createCoordinatesXFromData(jsonData) {
    var x = [];
    jsonData.forEach(element => {
        x.push(element.date);
    });
    return x
}
function createCoordinatesYFromData(jsonData) {
    var y = [];
    jsonData.forEach(element => {
        y.push(element.energyCounted);
    });
    return y
}


function plotMonthlyCaloriesIntake(context) {
    var trace1 = {
        type: 'bar',
        x: createCoordinatesXFromData(context),
        y: createCoordinatesYFromData(context),
        marker: {
            color: '#f4ed71',
            line: {
                width:2.5
            }
        }
    };
    console.log(createCoordinatesYFromData(context));

    var data = [ trace1 ];
    var layout = {
        title: 'Whole User Data',
        font: {size: 12,
                color: '#04030C',
        },
        hovermode:'closest',
        plot_bgcolor:"#383140",
        paper_bgcolor:"#CAC7d7",
        xaxis: {
            tickangle: -45,
            tickcolor: '#8a8604',
            gridcolor: "#8a8604"
          },
        yaxis: {
            gridcolor: "#8a8604",
          },
        showlegend: false,
        legend: {
            x: 0,
            y: 1.0,
            bgcolor: '#383140',
            bordercolor: '#04030C',
            borderwidth: 2,
          },
    };

    var config = {responsive: false}
    
    Plotly.newPlot(plotContainer, data, layout, config);

    plotContainer.on('plotly_hover', function(data){
        var infotext = data.points.map(function(d){
          return (d.data.name+': x= '+d.x+', y= '+d.y.toPrecision(3));
        });
    
    })


}

function fetchDataForUser() {

    const url = `http://127.0.0.1:8000/caloriestracker/getStats/`;
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
    })
    .then((response) => response.json())
    .then((data) => {
        plotMonthlyCaloriesIntake(data);

    })
    .catch((error) => {
    console.error('Error: ', error);
    if(error===401) {
        toggleLog();
    }
    });
}


toggleStatsBtn.addEventListener('click', function() {
    fetchDataForUser();
    wrapLemonContainerBtn.classList.toggle('toggleStatsBtnHidden');
    toggleStatsBtn.classList.toggle('toggleStatsBtnHidden');
})

wrapLemonContainerBtn.addEventListener('click', function() {
    fetchDataForUser();
    toggleStatsBtn.classList.toggle('toggleStatsBtnHidden');
    wrapLemonContainerBtn.classList.toggle('toggleStatsBtnHidden');
    lemonImage.classList.toggle('lemon-image')
})

