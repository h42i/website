window.onload = function() {
  var slider = document.getElementById('slider');
  var sources = ["/images/slider/slide1.jpg"
                ,"/images/slider/slide2.jpg"
                ,"/images/slider/slide3.jpg"
                ,"/images/slider/slide4.jpg"
                ,"/images/slider/slide5.jpg"
                ,"/images/slider/slide6.jpg"];

  var images = [];
  var index = 1;

  var display = window.getComputedStyle(slider)['display'];
  if (display !== 'none') {
    for (var i = 0; i < sources.length; i++) {
      images[i] = new Image;
      images[i].src = sources[i];
      console.log(sources[i]);
    }

    var progress = slider.getElementsByClassName('progress')[0];
    var delay = 5000;
    var time_last = new Date().getTime();
     
    setInterval(function() {
      var time_new = new Date().getTime();
      var time_diff = time_new - time_last;
      if (time_diff >= delay) {
        time_last = time_new;
        index = (index+1) % images.length;
        slider.style.backgroundImage = ("url(" + sources[index] + ")");
      }
      progress.style.width = (time_diff/delay*100 + '%')
    }, 10)
  }
};
