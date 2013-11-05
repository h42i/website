#!/usr/bin/env python
# -*- coding:utf8 -*-

# liest den Kalender von HaSi. Bei Fragen bitte an Simon wenden.
#
# python ical.py --summary  -- Terminübersicht mit Links auf die Kalenderseite
# python ical.py --full     -- Terminübersicht mit Beschreibungen
#
# Wenn keine URLs zu icals angegeben werden dann wird die URL des
# HaSi-Kalenders genutzt.

import sys, StringIO, subprocess, re, urllib
import datetime
import dateutil.rrule, dateutil.parser, dateutil.tz

urllist = [
   "https://www.google.com/calendar/ical/bhj0m4hpsiqa8gpfdo8vb76p7k%40group.calendar.google.com/public/basic.ics",
]

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
      if self["SUMMARY"]:
         r.append ("* %s: <a name=\"summary-%s\" href=\"/calendar/#item-%s\">%s</a>" % (str (self.get_time()[0].strftime ("__%d. %m. %Y__")), self["UID"], self["UID"], self["SUMMARY"]))

      return "\n\n".join (r)


   def longdesc (self):
      r = []
      if self["SUMMARY"]:
         r.append ("## <a name=\"item-%s\" href=\"/calendar/#summary-%s\">%s</a>" % (self["UID"], self["UID"], self["SUMMARY"]))

      r.append (str (self.get_time()[0].strftime ("__%d. %m. %Y, %H:%M Uhr__")) + "\n")
      if self["DESCRIPTION"]:
         r.append (self["DESCRIPTION"] + "\n")

      if self["LOCATION"]:
         r.append ("_Ort:_ " + self["LOCATION"])

      if self["URL"]:
         r.append ("_weitere Infos:_ [%s](%s)" % (self["URL"], self["URL"]))

      pending = self.get_time()[1:]
      if pending:
         r.append ("_Folgetermine:_ " +
                   ", ".join ([p.strftime ("%d. %m. %Y") for p in pending[:3]]) + [".", "…"][len (pending) > 3])
      return "\n\n".join (r)


   def __getitem__(self, key):
      return super (Event, self).get (key, None)


   def __setitem__(self, key, value):
      rdict = { 'n' : "\n" }
      value = re.sub ("\\\\(.)",
                      lambda x: rdict.get (x.group(1), x.group(1)), value)
      super (Event, self).__setitem__ (key, value)


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
   for url in urllist:
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

   summary_in  = "\n".join ([e.shortdesc() for e in el])
   p = subprocess.Popen ("kramdown",
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)
   summary_out, summary_err = p.communicate (summary_in)

   fulllist_in = "\n\n".join ([e.longdesc()  for e in el])
   p = subprocess.Popen ("kramdown",
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)
   fulllist_out, fulllist_err = p.communicate (fulllist_in)

   for f in sys.argv[1:]:
      data = open (f).read ()
      data2 = re.sub ("(?ms)(<!-- ical:summary -->).*?(<!-- /ical:summary -->)",
                      lambda x: x.group(1) + summary_out + x.group(2), data)
      data2 = re.sub ("(?ms)(<!-- ical:full -->).*?(<!-- /ical:full -->)", 
                      lambda x: x.group(1) + fulllist_out + x.group(2), data2)

      if data2 != data:
         outf = open (f, "w")
         outf.write (data2)
         outf.close ()

