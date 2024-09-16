const f = document.getElementById("form")
const inpt = document.getElementById("file")
const pred = document.querySelector(".pred")
const conf = document.querySelector(".conf")
const imgPreview = document.querySelector('.img-preview');

inpt.addEventListener('change', function(event) {
    const file = event.target.files[0]; // Get the selected file
    if (file) {
        const reader = new FileReader(); // Create a FileReader object
        reader.onload = function(e) {
            imgPreview.src = e.target.result; // Set the image preview source
        };
        reader.readAsDataURL(file); // Read the file as a data URL
    }
});

f.addEventListener('submit',function(e) {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', inpt.files[0]);

    for (let item of formData.entries()) {
      console.log(item[0], item[1]);
    }

    fetch('http://localhost:8000/detect',{
        method: "POST",
        body: formData,
    }).then(response => response.json()).then(response => {
        pred.innerHTML=`Disease Class : ${response['class']}`
        conf.innerHTML=`Confidence : ${(response['confidence'] * 100).toFixed(2)}%`
    });
})