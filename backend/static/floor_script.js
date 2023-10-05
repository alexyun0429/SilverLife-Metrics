
function menuOnClick() {
    document.getElementById("menu-bar").classList.toggle("change");
    document.getElementById("nav").classList.toggle("change");
    document.getElementById("menu-bg").classList.toggle("change-bg");
  }

// Dynamically change colors
function getRandomRedHue() {
  const redComponent = Math.floor(Math.random() * 256);
  const greenComponent = Math.floor(Math.random() * (256 - redComponent / 2)); // Reduce the green component
  const blueComponent = Math.floor(Math.random() * (256 - redComponent / 2));  // Reduce the blue component

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
  const greenComponent = Math.floor(Math.random() * (256 - (256 - redComponent) / 4)); // Favor the green component but less than red
  const blueComponent = Math.floor(Math.random() * (256 - redComponent) / 2); // Keep the blue component relatively low

  return `rgb(${redComponent}, ${greenComponent}, ${blueComponent})`;
}

function changeColor() {
  document.body.style.backgroundColor = getRandomRedHue();
}

/**
 * Fetch Patients using API
 */

function fetchPatient() {

}

// document.getElementById("data-output").innerHTML = '
// '