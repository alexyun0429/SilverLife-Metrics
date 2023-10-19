/**
 * Active popup to appear and blurs the background
 */
function toggle() {
  var blur = document.getElementById("blur");
  blur.classList.toggle("active");
  var popup = document.getElementById("popup");
  popup.classList.toggle("active");
}

/**
 *  Collects Form data, converts it to Json, and sends it to Flask endpoint.
 *  For add patient
 */
function submitForm() {
  const formData = new FormData(document.getElementById("patientForm"));

  // Send data as JSON to Flask endpoint.
  fetch("/api/addPatient", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        console.log("Patient added successfully!");
        // You might redirect to a success page or clear the form here
      } else {
        console.error("Failed to add patient.");
        // You might show an error message to the user here
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      // You might show an error message to the user here
    });
}

// For handling with the enabling and disabling of the submit button using the checkbox
var checkbox = document.querySelector("input[name=Confirm]");
var btn = document.querySelector("input[name=Submit]");

/**
 * Disables Submit button if check is left unticked
 */
checkbox.addEventListener("change", function () {
  if (this.checked) {
    btn.disabled = false;
  } else {
    btn.disabled = true;
  }
});
