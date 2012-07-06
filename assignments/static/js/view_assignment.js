var fileFieldCounter = 1;

function submitButtonClicked(event)
{
	var submissionForm = $("form#submit-assignment-form");
	submissionForm.submit();
}

function addSubmissionButtonClicked(event)
{
	var submissionForm = $("form#submit-assignment-form");
	submissionForm.css({ opacity : 0.0 }).animate({
		opacity	: 1.0,
		height	: "toggle"
	}, 300);

	var addSubmissionButton = $("#add-submission-button");
	addSubmissionButton.text("Submit");
	addSubmissionButton.unbind();
	addSubmissionButton.click(submitButtonClicked);
}

function addFileButtonClicked(event)
{
	$("<input>").attr({
		type	: "file",
		name	: "file" + (++fileFieldCounter)
	}).insertBefore("a#add-file-button");
}

$(document).ready(function() {
	// setup listeners
	$("#add-submission-button").click(addSubmissionButtonClicked);
	$("#add-file-button").click(addFileButtonClicked);
});
