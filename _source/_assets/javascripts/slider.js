window.onload = function() {
  var index = 0;
  var slider = document.getElementById('slider');
  var images = slider.getElementsByTagName('img');
  var progress = slider.getElementsByClassName('progress')[0];
  
  var time_last  = new Date().getTime();
  var delay = 5000;
  
  setInterval(function() {
    var time_new = new Date().getTime();
    var time_diff = time_new - time_last;
    if (time_diff >= delay) {
      time_last = time_new;
      index = (index+1) % images.length;
      for (var i = 0; i < images.length; ++i) {
        images[i].style.opacity= ((i == index) ? 1 : 0);
      }
    }
    progress.style.width = (time_diff/delay*100 + '%')
  }, 10)
};