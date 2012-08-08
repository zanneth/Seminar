var usernameIsUnique = false;

function createErrorElement(message)
{
	return $("<span>", {
		class	: "error",
		text	: message
	});
}

function validateRegistrationForm(event)
{
	var username	= $("#username").val();
	var first		= $("#first-name").val();
	var last		= $("#last-name").val();
	var email		= $("#email").val();
	var password1	= $("#password1").val();
	var password2	= $("#password2").val();

	// Clear errors if there are any.
	$("form#registration-form td > span.error").remove();

	var valid = true;

	if (username.length == 0) {
		var errEl = createErrorElement("You must enter a username.");
		$("#username-status").html(errEl);
		valid = false;
	}

	if (first.length == 0) {
		createErrorElement("You must enter a first name.").insertAfter("#first-name");
		valid = false;
	}

	if (last.length == 0) {
		createErrorElement("You must enter a last name.").insertAfter("#last-name");
		valid = false;
	}

	var emailRegex = new RegExp("[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,4}", "i");
	if (email.length == 0 || !emailRegex.test(email)) {
		createErrorElement("You must enter a valid email address.").insertAfter("#email");
		valid = false;
	}

	if (password1.length < 6) {
		createErrorElement("Your password must be at least 6 characters.").insertAfter("#password1");
		valid = false;
	} else if (password1 != password2) {
		createErrorElement("Passwords do not match.").insertAfter("#password2");
		valid = false;
	}

	return valid && usernameIsUnique;
}

function checkUsernameUniqueness(event)
{
	var username = $("#username").val();
	if (username.length == 0) {
		return;
	}
	
	usernameIsUnique = false;
	$("#username-status").html("Checking uniqueness...");

	$.ajax({
		type: "GET",
		url: "/api/register/check_username",
		data: { username : username }
	}).done(function (result) {
		var exists = !!eval("(" + result + ")");
		usernameIsUnique = !exists;

		if (!usernameIsUnique) {
			var errEl = createErrorElement("Username already exists.");
			$("#username-status").html(errEl);
		} else {
			$("#username-status").html("OK!");
		}
	});
}

$(document).ready(function() {
	$("form#registration-form").submit(validateRegistrationForm);
	$("#username").blur(checkUsernameUniqueness);
});
