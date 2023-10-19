/**
 * Displays Menu contents
 */
function menuOnClick() {
  document.getElementById("menu-bar").classList.toggle("change");
  document.getElementById("nav").classList.toggle("change");
  document.getElementById("menu-bg").classList.toggle("change-bg");
}

/**
 * Fetches patients from database of the specific floor
 * @param {string} floorNumber 
 */
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

/**
 * Populates the Floor databoard with the current patient of that floor
 * @param {data} patients 
 */
function updatePatientsUI(patients) {
  const outputDiv = document.getElementById("data-output");
  outputDiv.innerHTML = "";
  if (patients.length === 0) {
    outputDiv.innerHTML =
      "<div class='no-patients'>No patients found on this floor</div>";
  } else {
    patients.forEach((patient) => {
      // Card-container contains cards of patients on current floor
      //    Card-face front:
      //    - Contains Room number of patient,
      //    - photo with their respective face
      //    - name of patient
      //    Card-face back:
      //    - Contains Room number
      //    - Data of the patient
      //    Button pops up more details of the patient on the card
      //  Popup:
      //  - Close button
      //  - Patient Stress
      //  - Patient HRC
      //  - Patient Sleep
      //  - Patient details by graph
      const patientCardHTML = `
              <div class="card-container" onclick="flipCard(this)">
                <div data-modal-target="detailedPatients" class="patient-card">
                  <div class="card-face front">
                    <div class="patient-room">Room: ${patient.room_number}</div>
                    <img class="patient-photo" src="${patient.photo_path}" width="300" height="200" />
                    <div class="patient-name">${patient.first_name} ${patient.last_name}</div>
                  </div>

                  <div class="card-face back" id="back_${patient.user_access_token}">
                    <div class="patient-room">Room: ${patient.room_number}</div>
                    <div class="patientgraph">
                        <img id="${patient.user_access_token}_graph_back" src="data:image/png;base64,${patient.graph1}" />
                    </div>
                    <div>
                      <button type="button" onclick="togglePopup(event, 'popup_${patient.user_access_token}')">View More</button>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="popupDetails" id="popup_${patient.user_access_token}" style="display:none;">
                <div class="patientDetails_header">
                  <input
                    id="close"
                    type="image"
                    src="static/photos/Homepage/close.png"
                    alt="Close"
                    onclick="closePopup(event, 'popup_${patient.user_access_token}')"
                  />

                  <div class="Name_Room"></div>
                </div>

                <div class="patientdata">
                  <div class="patientblock" id="stressdata">
                    <div class="data">
                      <p>Stress</p>
                      <h3>192</h3>
                    </div>

                    <div class="img-div">
                      <img src="static/photos/Floor/patient_popup/stress.png" w />
                    </div>
                  </div>
                  <div class="patientblock" id="hrvdata">
                    <div class="data">
                      <p>HRV</p>
                      <h3>40</h3>
                    </div>
                    <div class="img-div">
                      <img
                        src="static/photos/Floor/patient_popup/icons8-heart-rate-100.png"
                      />
                    </div>
                  </div>
                  <div class="patientblock" id="sleepdata">
                    <div class="data">
                      <p>Sleep</p>
                      <h3>100</h3>
                    </div>
                    <div class="img-div">
                      <img src="static/photos/Floor/patient_popup/sleep.png" />
                    </div>
                  </div>
                </div>

                <p>Patient Details</p>
                <!-- Simulate Graph -->
                <div class="patientgraph">
                  <img id="${patient.user_access_token}_graph" src="data:image/png;base64,${patient.graph30}" />
                </div>
              </div>`;

      outputDiv.innerHTML += patientCardHTML;
    });
  }
}

/**
 * Toggles the visibility of a popup showing more details of patient associated with a patient ID.
 * @param {Event} e 
 * @param {string} patientId 
 * @returns 
 */

function togglePopup(e, patientId) {
  e.stopPropagation();
  var popup = document.getElementById(patientId);
  console.log("Toggling popup", patientId, popup); // Debug line

  // Toggle display and 'active' class
  if (popup.style.display === "none" || popup.style.display === "") {
    popup.style.display = "block";
  } else {
    popup.style.display = "none";
    return;
  }
  popup.classList.toggle("active");
}

/**
 * Toggles off the visibility of the popup showing more details of patient associated with a patient ID.
 * @param {Event} e 
 * @param {string} patientId 
 */

function closePopup(e, patientId) {
  console.log("closePopup called with patientId:", patientId); // Debug line

  e.stopPropagation();
  var popup = document.getElementById(patientId);
  console.log("Closing popup", patientId, popup); // Debug line

  // Hide the popup and remove 'active' class
  if (popup.style.display === "block") {
    popup.style.display = "none";
  }
  popup.classList.remove("active");
  resizeGraph(patientId, true);
}

function flipCard(element) {
  element.classList.toggle("flip");
  resizeGraph(element, false);
}
