window.onload = function() {
  var index = 0;
  var slider = document.getElementById('slider');
  var images = slider.getAttribute('data-images').split(',');
  console.log(images);
  slider.style.backgroundImage="url(\'" + images[0] + "\')"
  
  setInterval(function() {
    index = (index+1) % images.length;
    console.log(index);
    slider.style.backgroundImage="url(\'" + images[index] + "\')"
    console.log("tick");
  }, 5000)
};