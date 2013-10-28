function initialize(id) {
	console.log(id)
	var query = new google.visualization.Query("/customers/data/actions/" + id);
	query.send(function(response) {
		/*if (response.isError()) {
          alert('Error in query');
    }*/
    var data = response.getDataTable();
    console.log(response);
    document.getElementById('graph').innerHTML = data;
    plot(data)
	});
}

function plot(data) {
	var chart = new google.visualization.ScatterChart(document.getElementById('graph'));
	chart.draw(data, {
          title: 'Door activity over time',
          hAxis: {title: 'Time'},
          vAxis: {title: 'Activity'},
          legend: 'none'
        }
	);
}