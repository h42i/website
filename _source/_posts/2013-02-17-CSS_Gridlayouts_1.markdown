---
layout: post
title: CSS Gridlayouts (Teil 1)
category: blog
tags:
- Webdesign
---
# Theoretische Grundlage von Gridlayouts

## Whoot??

Als Gridlayouts bezeichnet man bei der Entwicklung von Websites ein aus Zeilen und Spalten bestehendes Grundgerüst zur Positionierung von Elementen. Die Verwendung eines Gridlayouts erspart es, bei jedem Webprojekt die Position einzelner Elemente manuell festzulegen.

<!-- break -->

## Beispiele

* [Twitter bootstrap](http://twitter.github.com/bootstrap/) enthält unter anderem auch ein 12-Spaltiges Gridsystem
* [Gridpak](http://gridpak.com/) ist ein online Gridgenerator mit dem es möglich ist, schnell eigene Grids zu erstellen 
* [l3 grid](https://github.com/l3kn/l3_grid) Meine eigene, leicht anpassbare Umsetzung eines Gridlayouts, geschrieben in .sass (dazu später mehr)
* [1140 css grid](http://cssgrid.net/) Ein weiteres vorgefertigtes Gridlayout

## Aufbau

Alle Beispiellayouts basieren auf zwei Hauptklassen:

1. `.row`
Unterteilt das Layout horizontal  
2. `.column_(1..n)`
Vertikale 'Blöcke' in n (meist 12) verschiedenen Breiten
wobei die columns wieder rows mit weiteren columns enthalten können, da die Breitenangaben relativ sind.

![layout](http://shared.l3kn.de/images/gridlayout.png)

### Warum 12?

Häufig unterteilen sich Gridlayouts in 12 columns, da sich die Zahl 12 gut in

> * zwei columns der Breite 6
> * drei columns der Breite 4
> * vier columns der Breite 3
> * sechs columns der Breite 2

teilen lässt.

Eine gröbere Unterteilung wäre aber auch mit 6 (teilbar durch 1,2,3 und 6) möglich,
feinere Layouts könnten sich in 24 Spalten (teilbar durch 1,2,3,4,6,8,12 und 24) unterteilen.





