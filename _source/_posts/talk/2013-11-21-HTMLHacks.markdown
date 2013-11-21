---
layout: post
title: HTML und CSS Hacks
category: talk
author: Hybr1s
talk:
  file: Shawn_Shure-CSS_und_HTML_Hacks.mp3
  duration: 00:38:18
---

<html>
<head>
<meta charset="utf-8" />

	<link href="http://hasi.it/podlove-web-player/static/podlove-web-player.css" rel="stylesheet" media="screen" type="text/css" />

	<script src="http://hasi.it/podlove-web-player/libs/html5shiv.js"></script>
	<script src="http://hasi.it/podlove-web-player/libs/jquery-1.9.1.min.js"></script>
	<script src="http://hasi.it/podlove-web-player/static/podlove-web-player.js"></script>
</head>

<body>
	<p>
		<audio id="testplayer1">
			<source src="http://files.hasi.it/podcast/Shawn_Shure-CSS_und_HTML_Hacks.mp3" type="audio/mpeg"></source>
		</audio>

		<script>
			$('#testplayer1').podlovewebplayer({
				poster: 'http://hasi.it/images/HaSi_Cover.png',
				title: 'HTML und CSS Hacks',
				permalink: 'http://hasi.it/talk/2013/11/21/HTMLHacks.html',
				subtitle: '',
				summary: '<p></p>',
				downloads: [{"name": "MPEG-1 Audio Layer III (MP3) High Quality","size": 5300,"url": "http://files.hasi.it/podcast/Shawn_Shure-CSS_und_HTML_Hacks.mp3","dlurl": "http://files.hasi.it/podcast/Shawn_Shure-CSS_und_HTML_Hacks.mp3"}],
				duration: '38:18.400',
				alwaysShowHours: true,
				startVolume: 0.8,
				width: 'auto',
				summaryVisible: false,
				timecontrolsVisible: false,
				sharebuttonsVisible: false,
				chaptersVisible: false
			});
		</script>
	</p>
</body>
</html>
<br />

<!-- break -->

Flexboxes, Pseudo-Selektoren, responsive Menüs und niedliche Katzenbilder:
Wie lassen sich mit den neuesten CSS-Modulen und durch kreative Kombination alter Elemente $(spannende? großartige? tolle?) Effekte ganz ohne JavaScript erzielen?
