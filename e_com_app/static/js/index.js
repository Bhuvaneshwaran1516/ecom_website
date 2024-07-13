function validateForm(event) {
    // Fetching values from inputs

    event.preventDefault();
    
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // Reset previous error messages
    document.getElementById("usernameError").textContent = "";
    document.getElementById("passwordError").textContent = "";

    // Flag to track if there are errors
    var hasError = false;

    // Validation for username
    if (username.trim() === "") {
        document.getElementById("usernameError").textContent = "Username is required";
        hasError = true;
    }

    // Validation for password
    if (password.trim() === "") {
        document.getElementById("passwordError").textContent = "Password is required";
        hasError = true;
    }

    // Prevent the form from submitting if there are errors
    if (hasError) {
        return false;
    }

    // Normally, you would submit the form here if no errors
    // For demonstration, we'll log a success message
    console.log("Form submitted successfully");

    // Clear form fields (optional)
    document.getElementById("loginForm").reset();

    // Prevent actual form submission
    return false;
}


