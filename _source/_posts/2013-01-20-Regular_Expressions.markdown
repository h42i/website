---
layout: post
title: Regular Expressions
category: blog
tags:
- Code
---
# Beschreibung

Als regulären Ausdruck _(regular expression oder Regex)_ bezeichnet man in der Informatik einen syntaktischen Regeln folgenden Ausdruck zur Beschreibung anderer Zeichenketten.

So beschreibt zum Beispiel der reguläre Ausdruck [abc] eine beliebig lange Folge der Zeichen 'a','b' und 'c'. 

<!-- break -->

# Zeichen

## Zeichenauswahlen

[abc]|'a', 'b' oder 'c'
[A-Z]|Zeichen aus dem Bereich von 'A' bis 'Z'
[^A-Z]|alle Zeichen außer dem Bereich 'A' bis 'Z'
 (_^_ in einer Zeichengruppe negiert den folgenden Ausdruck)
[A-Z0-9]|Großbuchstaben und Ziffern
.|ein beliebiges Zeichen

## Zeichenklassen

\d|Ziffer
\w|Ziffer/Buchstabe/'_'
\s|Whitespace (Leerzeichen, Tab, Newline)
\b|Leere Zeichenkette
der Klassenname großgeschrieben (\B) bezeichnet alle Zeichen die nicht der Klasse angehören

[:cntrl:]|Steuerzeichen
[:space:]|Whitespace
[:punct:]|Sonder- und Satzzeichen
[:alnum:]|Alphanumerische Zeichen
[:alpha:]|Buchstaben
[:lower:]|Kleinbuchstaben
[:upper:]|Großbuchstaben
[:xdigit:]|hexadezimale Ziffern
[:digit:]|dezimale Ziffern 	

## weitere (Meta)Zeichen

^|Zeilenanfang
<|leere Zeichenkette am Wortanfang
>|             "            ende
\n|Zeilenumbruch, Unix
\r|Zeilenumbruch, Mac
\r\n|Zeilenumbruch, Windows

Durch ein vorangestelltes '\' kann auch nach Metazeichen _z.B. '('_ gesucht werden


# Quantoren 

Quantoren können hinter einen Ausdruck geschrieben werden und beschreiben, wie oft er vorkommt.

?|optional _0..1_
+|min. 1*  _1..∞_
*|beliebig _0..∞_ (greedy, maximal mögliche Länge)
?*|beliebig _0..∞_ (non-greedy, minimal nötige Länge)
{n}|_n_
{n,}|_n..∞_
{n,m}|_n..m_
{0,m}|_0..m_

# Logik

(?=exp)|*exp* muss nachfolgend erfüllt sein, wird aber nicht angezigt 
(?!exp)|*exp* darf nachfolgend nicht erfüllt sein, wird aber nicht angezigt 
(?<=exp)|*exp* muss vorausgehend erfüllt sein, wird aber nicht angezigt 
(?<!exp)|*exp* darf vorausgehend nicht erfüllt sein, wird aber nicht angezeigt 

# Gruppierungen

(wort)|runde Klammern fassen Ausdrücke zusammen, diese Regex sucht nach 'wort'

# Beispiele

^[A-Z]|Ein Großbuchstabe am Zeilenanfang
eine IPv4 Adresse lässt sich grob durch ([0-9]{1,3}[.]?){4}|beschreiben
\(\d+\)|Eine Zahl in runden Klammern _z.B. '(42)'_
(?<=\()\d+(?=\))|wie oben, hier wird aber nur die Zahl ausgewählt _(die '23' in '(23)')_
((foo ))?(bar)(?(1)( baz))|akzeptiert nur 'bar' oder 'foo bar baz', aber nicht 'bar baz'


