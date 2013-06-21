---
layout: post
title: Guidelines
category: meta
---

## Philosophie / Meta

* Alle verwendeten Tools sollten Open-Source sein  
* Responsive Design -> keine Breitenangaben in __px__, immer __%__ oder __em__  
* Mobile first -> Das Stylesheet b ezieht sich auf die Version für Mobilgeräte,
alle Anpassungen für breitere Bildschirme finden in den media-queries am Ende 
der Datei statt  
* Ändert mal die breite eures Browserfensters, um zu sehen, warum der oben 
gewählte Ansatz sinnvoll ist.  
* Flat UI, möglichst keine Schatten oder Farbverläufe.  
* Sauberer Quellcode, "Hacks" wie die _.group_-Kalsse sollten erklärt werden.  
* redundater Code sollte vermieden werden -> includes Verwendern  

## Grab the tools

~~~ bash
$paketmanager $install ruby rubygems git
gem install jekyll sass jekyll-assets coderay kramdown
~~~

* Jekyll - Rubybasierter static site generator  
* Kramdown - ein Markdown superset (sowas wie LaTeX, nur einfacher)
* Sass - CSS-Preprocessor, -Syntax +Variablen +fancy Funktionen
* Coderay - Syntax Highlighting
* jekyll-assets - eine Asset-Pipeline für Jekyll


## Get the git

~~~ bash
git clone ssh://h42i@hasi.it/home/hasi/git/jekyll.git
~~~

## Befehle

~~~ bash
jekyll serve --watch
~~~
Startet einen Webserver auf Port 4000 und generiert die Seite nach Änderungen 
automatisch neu

~~~ bash
jekyll build
~~~
Wie oben, nur nicht automatisch und ohne Webserver ;)

~~~ bash
git commit -am '$Beschreibung'
git push
~~~
Um die Änderungen auf den Server hochzuladen, sollte nach 5sec sichtbar sein.

Wenn das Ganze am Anfang nicht klappt hilft ein einmaliges

~~~ bash
git push origin master
~~~

## Aufbau

~~~ text
.
├── _config.yml - Konfigurationsdatei, z.B. für die Menüstruktur
├── _source - Quelldateien
|	├── _assets
|	|   ├── stylesheets
|	|	|   ├── main.sass - Hauptstylesheet
|	|	|   └── icons.sass, normalize.css - don't touch this!
|	|   ├── images - alle Bilder kommen hier rein
|	|   └── fonts
|	├── _includes - Code snippets die häufig verwendet werden
|	|   └── ...
|	├── _layouts - Layouts, werden im header einer Datei definiert
|	|   ├── default.html - Layout der gesamten Seite 
|	|   └── post.html - Layout für die Seite eines Blogposts
|	├── _posts
|	|   ├── YYYY-MM-DD-Name_mit_underscores_statt_spaces.markdown
|	|   └── YYYY-MM-DD-Anderer_Beitrag
|	├── index.html - Startseite
|	└── $name - z.B. hasi.it/blog/
|	    └── index.html - Unterseite
└── _site - Zielverzeichnis, don't touch this!
~~~

## Docs
[Jekyll](http://jekyllrb.com/docs/home/)  
[Kramdown](http://kramdown.rubyforge.org/)  

## Misc. Info

Markdown tut manchmal komische Dinge, Zeilenumbrüche werden mit 2x Space am Ende
der Zeile erzeugt.
