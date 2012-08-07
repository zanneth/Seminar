var fileFieldCounter = 1;

function createCommentElement(author, body)
{
	var commentEl = $("<div>", {
		class : "comment"
	});

	$("<h1>", {
		class	: "comment-author",
		text	: author
	}).appendTo(commentEl);

	$("<p>", {
		class	: "comment-body",
		text	: body
	}).appendTo(commentEl);

	$("<div>", {
		class	: "comment-details-container"
	}).appendTo(commentEl).append($("<span>", {
		class	: "comment-date",
		text	: "Posted just now"
	}));

	return commentEl;
}

function createAddReplyElement()
{
	var replyEl = $("<div>", {
		class	: "comment-reply-container"
	});

	$("<textarea>", {
		cols	: 40,
		rows	: 5,
		id		: "comment-body"
	}).appendTo(replyEl);

	$("<input>", {
		id		: "add-reply-button",
		type	: "button",
		value	: "Add Reply"
	}).appendTo(replyEl).click(addReplyButtonClicked);

	$("<input>", {
		id		: "cancel-reply-button",
		type	: "button",
		value	: "Cancel"
	}).appendTo(replyEl).click(cancelReplyButtonClicked);

	return replyEl;
}

function showError(afterElement, errorMessage)
{
	var errEl = afterElement ? afterElement.next(".error") : null;
	if (!errEl) {
		errEl = $("<span>", {
			class	: "error",
			text	: errorMessage
		});

		if (afterElement) {
			errEl.insertAfter(afterElement);
		}
	} else {
		errEl.text(errorMessage);
	}

	return errEl;
}

function submitButtonClicked(event)
{
	var submissionForm = $("form#submit-assignment-form");
	var filesEl = $(".file-input", submissionForm);

	// Validate the form
	var valid = false;
	for (var i = 0; i < filesEl.length; ++i) {
		valid |= $(filesEl[i]).val().length > 0;
	}
	valid |= $("#submission-comments").val().length > 0;

	if (valid) {
		submissionForm.submit();
	} else {
		if (!$("#submission-error").length) {
			var errEl = showError(null, "You must add at least one file or enter a comment.");
			$("<div>", {
				id	: "submission-error",
				css	: { "padding-bottom" : "20px" }
			}).append(errEl).insertAfter(submissionForm);
		}
	}
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
		class	: "file-input",
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

	if (body.length == 0) {
		showError(addCommentButton, "You must enter a comment body.");
		return false;
	}

	addCommentButton.attr("disabled", true);

	$.ajax({
		type	: "POST",
		url		: "/api/assignments/add_comment",
		data	: { "body" : body, "assignment_id" : assignmentID }
	}).done(function (result) {
		var commentEl = createCommentElement(username, body);
		$("div#comments-container").append(commentEl);
		$("#comment-body").val("");

		var noCommentEl = $("#no-comments");
		if (noCommentEl.length) {
			noCommentEl.remove();
		}
	}).fail(function (result) {
		showError(addCommentButton, "There was an error posting your comment. Please try again later.");
		console.log(result);
	}).always(function (result) {
		addCommentButton.removeAttr("disabled");
	});

	return false;
}

function addReplyButtonClicked(event)
{
	var commentEl = $(event.target).closest(".comment");
	var commentID = parseInt($(".comment-id", commentEl).text());
	var assignmentID = $("#assignment-id").val();
	var addReplyButton = $(event.target);
	var username = $("#username").val();
	var body = $("#comment-body", commentEl).val();

	if (body.length == 0) {
		showError(addReplyButton, "You must enter a reply body.");
		return false;
	}

	addReplyButton.attr("disabled", true);

	$.ajax({
		type	: "POST",
		url		: "/api/assignments/add_comment",
		data	: {
			"body"			: body,
			"assignment_id"	: assignmentID,
			"parent_id"		: commentID
		}
	}).done(function (result) {
		var replyEl = createCommentElement(username, body);
		commentEl.append(replyEl);
		$(".comment-reply-container", commentEl).remove();
	}).fail(function (result) {
		showError(addReplyButton, "There was an error posting your reply. Please try again later.");
		console.log(result);
	}).always(function (result) {
		addReplyButton.removeAttr("disabled");
	});

	return false;
}

function cancelReplyButtonClicked(event)
{
	var target = $(event.target);
	target.parent(".comment-reply-container").remove();
}

function replyButtonClicked(event)
{
	var target = $(event.target);
	var commentEl = target.closest(".comment");
	if (commentEl.find(".comment-reply-container").length == 0) {
		var replyEl = createAddReplyElement();
		replyEl.insertAfter($("> .comment-details-container", commentEl));
	}
}

$(document).ready(function() {
	// setup listeners
	$("#add-submission-button").click(addSubmissionButtonClicked);
	$("#add-file-button").click(addFileButtonClicked);
	$("#add-comment-button").click(addCommentButtonClicked);
	$(".comment-reply-button").click(replyButtonClicked);
});
