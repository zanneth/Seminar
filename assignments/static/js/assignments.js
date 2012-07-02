var selectedMonth = 0;
var selectedYear  = 0;

function equalizeCalendarCells()
{
	var calendarCells = $("div.assignment-calendar > table td");
	calendarCells.height(calendarCells.width());
}

function loadCalendar(month, year)
{
	$.ajax({
		type: "GET",
		url: "/assignments/calendar.html",
		data: { month : month, year : year }
	}).done(function (calendarHTML) {
		$("div.assignment-calendar").html(calendarHTML);
		equalizeCalendarCells();
	});
}

function calendarLeftArrowButtonClicked(event)
{
	selectedMonth--;
	if (selectedMonth <= 0) {
		selectedMonth = 12;
		selectedYear--;
	}

	loadCalendar(selectedMonth, selectedYear);
}

function calendarRightArrowButtonClicked(event)
{
	selectedMonth++;
	if (selectedMonth > 12) {
		selectedMonth = 1;
		selectedYear++;
	}

	loadCalendar(selectedMonth, selectedYear);
}

$(document).ready(function() {
	// equalize height of calendar table cells
	equalizeCalendarCells();

	// animate right calendar panel
	var slideAmount = 5;
	var el = $("div#assignments-right-panel");
	el.css({top : slideAmount + "px", opacity : 0.25});
	el.animate({top : -slideAmount + "px", opacity : 1}, 300);

	// retrieve server month and year
	selectedMonth = parseInt($(".servertime-month").text());
	selectedYear = parseInt($(".servertime-year").text());

	// attach event listeners to calendar arrow buttons
	$(".calendar-left").click(calendarLeftArrowButtonClicked);
	$(".calendar-right").click(calendarRightArrowButtonClicked);
});
