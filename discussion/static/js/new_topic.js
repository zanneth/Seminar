function createErrorElement(message)
{
	var errEl = $("<span>", {
		"class"	: "error",
		"text"	: message
	});

	return errEl;
}

function validateNewTopicForm(event)
{
	var title = $("input#topic-title").val();
	var body = $("textarea#topic-body").val();

	var err = null;
	if (title.length == 0) {
		err = createErrorElement("You must enter a topic title.");
	} else if (body.length == 0) {
		err = createErrorElement("You must enter a topic body.");
	}

	if (err) {
		var container = $("#submit-container");
		if (container.has(".error")) {
			$(".error", container).remove();
		}

		container.append(err);
		return false;
	}

	return true;
}

$(document).ready(function() {
	$("form#new-topic-form").submit(validateNewTopicForm);
});
