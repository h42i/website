window.onload = function() {
  var index = 0;
  var slider = document.getElementById('slider');
  var images = slider.getAttribute('data-images').split(',');
  console.log(images);
  
  //setInterval(function() {
    slider.style.backgroundImage="url(\'" + images[0] + "\')"
    console.log("tick");
  //}, 5000)
};