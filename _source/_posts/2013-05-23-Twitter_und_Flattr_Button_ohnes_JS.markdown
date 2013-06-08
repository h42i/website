---
layout: post
title: Twitter und Flattr Buttons ohne Javascript
category: blog
tags:
- Jekyll
- Webdesign
---
# Go home JS, you are drunk!

Normalerweise werden Flattr- und Twitterbuttons mit einem html-Anker definiert und dann durch Javascripts nachgeladen, 
obwohl normale Links viel einfacher und ressourcenschonender wären...

<!-- break -->

Der Vorteil dieser obskuren Scripts ist, dass neben dem Button auch die Anzahl der Nutzer, die ihn bereits geklickt haben,
angezeigt wird, wobei auch dies im Fall von Twitter kaum funktioniert.

Nachteile hingegen sind, dass Javascript erlaubt sein muss, um die Buttons anzuzeigen, die Verwenung von komische html Elemente und unkontrolliert nachlandende Dateien.
Außerdem kann das Aussehen der Buttons nicht (nur schwierig) angepasst werden.
Auch beim Blick in die Chrome Developer Tools (oder ähnliche Werkzeuge) wird schnell klar, dass diese Variante bestenfalls unelegant ist.

Obwohl der restliche Inhalt der Seite (dank gzip und code compression) in unter einer Sekunde geladen ist, benötigen die beiden Buttons mit dazugehörigem Javascript noch einmal drei Sekunden.

## Die Lösung

Laut der [Flattr Developer-docs](http://developers.flattr.net/auto-submit/) ist es möglich über einfache Links Inhalte zu flattrn.
Auch die Javascripts, die Twitter uns andrehen möchte, erzeugen letztendlich nur einen Link in dessen Parametern alle wichtigen Informationen enthalten sind, bis jetzt konnte
ich dafür aber keine offizielle Dokumentation finden.

Eine einfache Möglichkeit die Funktion des "tweet-this" Buttons nachzuempfinden sieht so aus:  
`{% raw %}https://twitter.com/intent/tweet?url=[URL]&via=[USERID]{% endraw %}`  
  
bei Flattr verhält es sich ähnlich, hier sollte aber noch eine Titelbeschreibung hinzugefügt werden:  
`{% raw %}https://flattr.com/submit/auto?user_id=[USERID]&url=[URL]&title=[TITEL]{% endraw %}`

## Als Jekyll Include

Der Static Site Generator [Jekyll](http://jekyllrb.com/), auf dem u.A. diese Website basiert, bietet die Möglichkeit sogenannte __Includes__ festzulegen um häufig wiederholten Code 
nur an einer Stelle anpassen zu müssen.

_\_includes/social.html_

~~~ html
{% raw %}
{% if post %}
    {% assign this = post %}
{% else %}
    {% assign this = page %}
{% endif %}

<a class="button" href="https://twitter.com/intent/tweet?url=http://www.l3kn.de{{ this.url }}&via=l3kn">
    tweet
</a>

<a class="button" href="https://flattr.com/submit/auto?user_id=l3kn&url=http://www.l3kn.de{{ this.url }}&title={{ this.title }}">
    flattr this
</a>
{% endraw %}
~~~

> Ich würde mich natürlich auch über fremde Flattrs freuen, die Parameter der URLs sollten aber noch angepasst werden ;)

Enthält das `_includes`-Verzeichnis die obenstehende Datei können Posts und einzelne Seiten durch ein einfaches   

~~~ html
{% raw %}{% include social.html %}{% endraw %}
~~~

mit Tweet- und Flattrbuttons versehen werden.  
Die entstehenden Links können dann durch Einfügen von Bildern oder Anpassungen im CSS individualisiert werden.
