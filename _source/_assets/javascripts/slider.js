window.onload = function() {
  var slider = document.getElementById('slider');
  var images = slider.getElementsByTagName('img');
  var progress = slider.getElementsByClassName('progress')[0];
  var delay = 5000;
  var time_last  = new Date().getTime();
  var index = images.length - 1;
  
  setInterval(function() {
    var time_new = new Date().getTime();
    var time_diff = time_new - time_last;
    if (time_diff >= delay) {
      time_last = time_new;
      index = (index+1) % images.length;
      console.log(index);
      for (var i = 0; i < images.length; i++) {
        images[i].style.opacity= ((i == index) ? 1 : 0);
      }
    }
    progress.style.width = (time_diff/delay*100 + '%')
  }, 10)
};