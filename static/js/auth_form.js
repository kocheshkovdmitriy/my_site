function openForm(id_form) {
    if (id_form == 'myForm') {
      document.getElementById('myForm').style.display = "block";
      document.getElementById('myForm1').style.display = "none";
    } else {
      document.getElementById('myForm1').style.display = "block";
      document.getElementById('myForm').style.display = "none";
    }
}

function closeForm(id_form) {
    document.getElementById(id_form).style.display = "none";
}

