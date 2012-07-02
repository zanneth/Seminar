var currentTime = 0;

function updateServerTimeView()
{
	var date = new Date(1000 * currentTime);
	var formatted = $.format.date(date.toString(), "ddd MMMM dd, yyyy h:mm:ss a");
	$("#servertime").html(formatted);
}

function serverTimeUpdateCallback()
{
	currentTime++;
	updateServerTimeView();
}

$(document).ready(function() {
	// Setup servertime view
	currentTime = parseInt($(".servertime-epoch").text());
	updateServerTimeView();
	setInterval(serverTimeUpdateCallback, 1000);
});
