function toggle(){
    var blur =document.getElementById('blur');
    blur.classList.toggle('active')
    var popup = document.getElementById("popup");
    popup.classList.toggle("active");
}

/**
 *  Collects Form data, converts it to Json, and sends it to Flask endpoint.
 */
function submitForm() {
    // Creates object and inserts values from respective attributes in HTML
    const data = {
        ids: document.getElementById('ids').value,
        fname: document.getElementById('fname').value,
        lname: document.getElementById('lname').value,
        rnum: document.getElementById('rnum').value
    }; 

    // Send data as JSON to Flask endpoint.
    fetch('/api/addPatient', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.status === "success") {
            // Handle success, maybe show a message or redirect
        } else {
            // Handle error
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
