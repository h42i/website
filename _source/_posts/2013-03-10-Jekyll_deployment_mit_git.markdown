---
layout: post 
title: Jekyll Deployment
category: blog
tags:
- Webdesign
- Git
- Jekyll
---

## Einleitung

Da Jekyll nur auf statischen Dateien basiert, bietet es sich an, die gesamte Website mit `git` zu deployen.
Natürlich ist es möglich, das alle nötigen Dateiens erst auf dem Webserver generieren zu lassen, dazu müssten dort aber auch alle genutzten Erweiterungen _(assets, coderay, sass)_ installiert sein, was nicht immer problemlos möglich ist.
Deshalb erzeuge ich die Seite lokal und pushe dann die Änderungen auf meinen [Uberspace](www.uberspace.de)

<!-- break -->

## Aufbau

Mein Aufbau besteht aus 3 .git-repositories, von denen sich eins lokal auf meinem PC und zwei auf meinem uberspace befinden.

### Lokal

Das lokale Repository ist ein Clone des **bare-Repos** auf dem Server und kann mit

~~~ bash
git clone ssh://<name>@<server>/home/<name>/git/jekyll.git
~~~

angelegt werden.
Damit Jekyll die generierten Dateien dort speichert muss der *directory:*-Pfad in der `_config.yml` Datei angepasst werden.  

~~~ yaml
directory: ../jekyll/
~~~

> __Achtung__
> Hier muss ein Ordner *(_site)* innerhalb des Repos angegeben werden, da sonst bei jedem Ausführen von `jekyll` auch der `.git` gelöscht würde.

### Remote

Auf dem Server befinden sich ein **bare-Repo** an das die von `jekyll` generierte Seite gepusht werden. Dieses wird mit 

~~~ bash
cd ~  
mkdir git
cd git   
mkdir jekyll.git
cd jekyll.git
git init --bare
~~~

erzeugt.

In `~/html/` befindet sich ein Clone des **bare-Repos**  

~~~ bash
git clone ~/git/jekyll.git
~~~

der mit einem git-hook im **bare-Repo** nach jedem Commit aktualisiert wird.

~~~ bash
mv ~/git/jekyll.git/hooks/post-receive.sample ~/git/jekyll.git/hooks/post-receive
vim ~/git/jekyll.git/hooks/post-receive 
~~~

In diese Datei muss folgendes Script eingefügt werden:

~~~ bash
#!/bin/sh
cd $HOME/html/jekyll/
git --git-dir $HOME/html/jekyll/.git pull
~~~

Sobald nun Änderungen aus dem lokalen Repo an das **bare-Repo** gepusht werden, aktualisiert sich auch das Repo im `html/` Ordner.

> `--git-dir $HOME/html/jekyll/.git` ist nötig, da `git` sich sonst, obwohl das Verzeichnis geändert wurde, auf das ursprüngliche Repo (jekyll.git) bezieht.

Nun muss nurnoch jeder Aufruf der Website (*hier l3kn.de*) an den Ordner `html/jekyll/` weitergeleitet werden.

~~~ bash
cd /var/www/virtual/<name>/
ln -s html/jekyll/ <url> 
ln -s html/jekyll/ www.<url> 
~~~

Treten beim ersten Pushen in das neue Repo Fehler auf hilft meist ein einmaliges

~~~ bash
git push origin master
~~~
