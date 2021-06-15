function displayLoadingSpinner(isDisplayed) {
  var spinner = document.getElementById("id_loading_spinner");
  if (isDisplayed) spinner.style.display = "block";
  else spinner.style.display = "none";
}
