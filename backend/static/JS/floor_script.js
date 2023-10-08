function menuOnClick() {
  document.getElementById("menu-bar").classList.toggle("change");
  document.getElementById("nav").classList.toggle("change");
  document.getElementById("menu-bg").classList.toggle("change-bg");
}

// Dynamically change colors
function getRandomRedHue() {
  const redComponent = Math.floor(Math.random() * 256);
  const greenComponent = Math.floor(Math.random() * (256 - redComponent / 2)); // Reduce the green component
  const blueComponent = Math.floor(Math.random() * (256 - redComponent / 2)); // Reduce the blue component

  return `rgb(${redComponent}, ${greenComponent}, ${blueComponent})`;
}

function getRandomGreenHue() {
  const greenComponent = Math.floor(Math.random() * 256);
  const redComponent = Math.floor(Math.random() * (256 - greenComponent / 2)); // Reduce the red component
  const blueComponent = Math.floor(Math.random() * (256 - greenComponent / 2)); // Reduce the blue component

  return `rgb(${redComponent}, ${greenComponent}, ${blueComponent})`;
}

function getRandomOrangeHue() {
  const redComponent = Math.floor(Math.random() * 256);
  const greenComponent = Math.floor(
    Math.random() * (256 - (256 - redComponent) / 4)
  ); // Favor the green component but less than red
  const blueComponent = Math.floor((Math.random() * (256 - redComponent)) / 2); // Keep the blue component relatively low

  return `rgb(${redComponent}, ${greenComponent}, ${blueComponent})`;
}

function changeColor() {
  document.body.style.backgroundColor = getRandomRedHue();
}

/**
 * Fetch Patients using API
 */

function fetchPatient() {}

// document.getElementById("data-output").innerHTML = '
// '

function updatePatientsData(floorNumber) {
  fetch(`/api/floor?number=${floorNumber}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok" + response.statusText);
      }
      return response.json();
    })
    .then((data) => {
      console.log("Fetched data: ", data); // Debug line
      updatePatientsUI(data);
    })
    .catch((error) => {
      console.error("Error fetching patient data:", error);
    });
}

function updatePatientsUI(patients) {
  const outputDiv = document.getElementById("data-output");
  outputDiv.innerHTML = "";
  if (patients.length === 0) {
    outputDiv.innerHTML =
      "<div class='no-patients'>No patients found on this floor</div>";
  } else {
    patients.forEach((patient) => {
      const patientCardHTML = `
              <div class="patient-card">

                  <div class="patient-room">Room: ${patient.room_number}</div>
                  
                  <img src="${patient.photo_path}" width="300" height="200" />
                  <div class="patient-name">${patient.first_name} ${patient.last_name}</div>
                  
              </div>`;
      outputDiv.innerHTML += patientCardHTML;
    });
  }
}
