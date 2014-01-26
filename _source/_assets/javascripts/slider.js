window.onload = function() {
  var index = 0;
  var slider = document.getElementById('slider');
  var images = slider.getElementsByTagName('img');
  
  setInterval(function() {
    index = (index+1) % images.length;
    for (var i = 0; i < images.length; ++i) {
      images[i].style.opacity= ((i == index) ? 1 : 0);
    }
  }, 5000)
};