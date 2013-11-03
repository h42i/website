#!/usr/bin/env python
# -*- coding:utf8 -*-

# liest den Kalender von HaSi. Bei Fragen bitte an Simon wenden.
#
# python ical.py --summary  -- Terminübersicht mit Links auf die Kalenderseite
# python ical.py --full     -- Terminübersicht mit Beschreibungen
#
# Wenn keine URLs zu icals angegeben werden dann wird die URL des
# HaSi-Kalenders genutzt.

import sys, re, urllib
import datetime
import dateutil.rrule, dateutil.parser, dateutil.tz

now = datetime.datetime.now (dateutil.tz.tzutc ())

def simple_tzinfos (abbrev, offset):
   if not abbrev and not offset:
      return dateutil.tz.tzlocal ()
   elif abbrev == "UTC" and offset == 0:
      return dateutil.tz.tzutc ()
   else:
      print "simple_tzinfos:", abbrev, offset
   return 0



class Event (dict):
   def shortdesc (self):
      r = []
      if self.has_key ("SUMMARY"):
         r.append ("* <a href=\"/calendar/#%s\">%s: %s</a>" % (self["UID"], str (self.get_time()[0].strftime ("__%d. %m. %Y__")), self["SUMMARY"]))

      return "\n\n".join (r)


   def longdesc (self):
      r = []
      if self.has_key ("SUMMARY"):
         r.append ("## <a name=\"%s\">%s</a>" % (self["UID"], self["SUMMARY"]))

      r.append (str (self.get_time()[0].strftime ("__%d. %m. %Y, %H:%M Uhr__")) + "\n")
      if self.has_key ("DESCRIPTION") and self["DESCRIPTION"]:
         def unq (x):
            rdict = {
               'n' : "\n",
            }
            return rdict.get (x.group(1), x.group(1))
         txt = self["DESCRIPTION"] + "\n"
         txt = re.sub ("\\\\(.)", unq, txt)
         r.append (txt)

      if self.has_key ("LOCATION") and self["LOCATION"]:
         r.append ("_Ort:_ " + self["LOCATION"])

      if self.has_key ("URL") and self["URL"]:
         r.append ("_weitere Infos:_ [%s](%s)" % (self["URL"], self["URL"]))

      pending = self.get_time()[1:]
      if pending:
         r.append ("_Folgetermine:_ " +
                   ", ".join ([p.strftime ("%d. %m. %Y") for p in pending[:3]]) + [".", "…"][len (pending) > 3])
      return "\n\n".join (r)


   def __lt__ (self, other):
      return self.get_time ()[0] < other.get_time ()[0]


   def is_pending (self):
      return now < self.get_time ()[0]


   def get_time (self):
      if self.has_key ("DTSTART") and self.has_key ("RRULE"):
         rr = dateutil.rrule.rrulestr ("DTSTART:%s\nRRULE:%s\n" % (self["DTSTART"], self["RRULE"]), tzinfos = simple_tzinfos)
         pending = rr.between (now, now + datetime.timedelta (120))
         return [ p.astimezone (dateutil.tz.tzlocal ()) for p in pending]

      if self.has_key ("DTSTART"):
         dts = dateutil.parser.parse (self["DTSTART"], tzinfos = simple_tzinfos)
         return [ dts ]

      return [ now ]



if __name__ == '__main__':
   args = set (sys.argv[1:])
   do_summary = False
   do_fulllist = False

   if "--summary" in args:
      do_summary = True

   if "--full" in args:
      do_fulllist = True

   if not do_summary and not do_fulllist:
      do_fullist = True

   args -= set (["--summary", "--full"])

   if not args:
      args = set (["https://www.google.com/calendar/ical/bhj0m4hpsiqa8gpfdo8vb76p7k%40group.calendar.google.com/public/basic.ics"])

   for url in args:
      data = urllib.urlopen (url).read()

      data = data.replace ("\r\n", "\n")
      data = data.replace ("\n\r", "\n")
      data = data.replace ("\n ", "")

      lines = [l.strip () for l in data.split ("\n")]

      eventlist = []
      cur_event = None

      for l in lines:
         if not l:
            continue

         extra = None
         key, value = l.split (":", 1)

         if ";" in key:
            key, extra = key.split (";", 1)

         if key == "BEGIN" and value == "VEVENT":
            cur_event = Event()
            continue
         
         if key == "END" and value == "VEVENT":
            eventlist.append (cur_event)
            cur_event = None
            continue
         
         if cur_event != None:
            cur_event[key] = value

   eventlist.sort ()

   el = [ e for e in eventlist if e.is_pending() ]

   if do_summary:
      for e in el:
         print e.shortdesc()

      if do_fulllist:
         print "\n\n<hr />\n"

   if do_fulllist:
      for e in el:
         print e.longdesc()
         print

