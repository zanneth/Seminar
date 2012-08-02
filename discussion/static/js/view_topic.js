function validateReplyForm(event)
{
	var body = $("textarea#post-body").val();
	if (body.length == 0) {
		var form = $("form#new-post-form");
		$("<span>", {
			class	: "error",
			text	: "You must enter a reply body."
		}).appendTo(form);

		return false;
	}

	return true;
}

$(document).ready(function() {
	$("form#new-post-form").submit(validateReplyForm);
});
