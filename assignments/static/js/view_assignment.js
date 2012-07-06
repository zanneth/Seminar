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

function addCommentButtonClicked(event)
{
	var body = $("#comment-body").val();
	var assignmentID = $("#assignment-id").val();
	var username = $("#username").val();
	var addCommentButton = $(event.target);

	addCommentButton.attr("disabled", true);

	$.ajax({
		type	: "POST",
		url		: "/api/assignments/add_comment",
		data	: { "body" : body, "assignment_id" : assignmentID }
	}).done(function (result) {
		var commentEl = $("<div>");
		var authorEl = $("<h1>").text(username).addClass("comment-author");
		var bodyEl = $("<p>").text(body).addClass("comment-body");

		commentEl.append(authorEl);
		commentEl.append(bodyEl);
		commentEl.addClass("comment");
		$("div#comments-container").append(commentEl);

		$("#comment-body").val("");
	}).fail(function (result) {
		$("<span class='error'>There was an error posting your comment. Please try again later.</span>")
			.insertAfter("#add-comment-button");
	}).always(function (result) {
		addCommentButton.removeAttr("disabled");
	});

	return false;
}

$(document).ready(function() {
	// setup listeners
	$("#add-submission-button").click(addSubmissionButtonClicked);
	$("#add-file-button").click(addFileButtonClicked);
	$("#add-comment-button").click(addCommentButtonClicked);
});
