function validateReplyForm(event)
{
	var body = $("textarea#post-body").val();
	if (body.length == 0) {
		var form = $("form#new-post-form");
		$("<span>", {
			"class"	: "error",
			"text"	: "You must enter a reply body."
		}).appendTo(form);

		return false;
	}

	return true;
}

function confirmDeletePost(event)
{
	return confirm("Are you sure you want to delete this post?");
}

$(document).ready(function() {
	$("form#new-post-form").submit(validateReplyForm);
	$("div#delete-post > a").click(confirmDeletePost);
});
