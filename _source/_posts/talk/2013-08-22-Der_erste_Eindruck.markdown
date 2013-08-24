---
layout: post
title: Der erste Eindruck
category: talk
author: Hybr1s
talk:
  file: Kati-Der_erste_Eindruck.mp3
  duration: 01:29:04
---
Der erste Eindruck - du hast nur eine Chance!
Kati hat uns an ihrer langjährigen Erfahrung der Selbstdarstellung und Präsentation teilhaben lassen: Was kann und sollte man beachten? Wie stelle ich mich dar? 

    <header><h2>media</h2></header>
    {% if post.talk.file %}
      <audio controls>
      <source src={{ site.podcast.path }}{{ post.talk.file }} type="audio/mpeg">
      Your browser does not support this audio format.
      </audio>
      <a href="{{ site.podcast.path }}{{ post.talk.file }}" class="button">Play (or download)</a>
    {% endif %}
    {% if post.talk.video %}
      <a href="{{ post.talk.video }}" class="button">Video</a>
    {% endif %}
    {% if post.talk.slides %}
      <a href="{{ post.talk.slides }}" class="button">Slides</a>
    {% endif %}
