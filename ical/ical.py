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

default_url = "https://www.google.com/calendar/ical/bhj0m4hpsiqa8gpfdo8vb76p7k%40group.calendar.google.com/public/basic.ics"

calendars = {}

now = datetime.datetime.now (dateutil.tz.tzutc ())


def kramdown (input):
   p = subprocess.Popen ("kramdown",
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)
   out, err = p.communicate (input)
   return out



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

      return "\n\n".join (r) + "\n"


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
      return "\n\n".join (r) + "\n"


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
         return [ dts.astimezone (dateutil.tz.tzlocal ()) ]

      return [ now.astimezone (dateutil.tz.tzlocal ()) ]



class Calendar(object):
   def __init__ (self, url=None):
      if not url:
         url = default_url

      self.url = url

      data = urllib.urlopen (self.url).read()

      # normalize lineends
      data = data.replace ("\r\n", "\n").replace ("\n\r", "\n")
      # ical continuation lines
      data = data.replace ("\n ", "")

      lines = [l.strip () for l in data.split ("\n")]

      self.eventlist = []
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
            self.eventlist.append (cur_event)
            cur_event = None
            continue
         
         if cur_event != None:
            cur_event[key] = value

      self.eventlist.sort ()


   def get_summary (self, limit=-1):
      el = [ e for e in self.eventlist if e.is_pending() ]
      if limit > 0:
         el = el[:limit]
      summary  = "\n".join ([e.shortdesc() for e in el])
      return kramdown (summary)


   def get_fulllist (self, limit=-1):
      el = [ e for e in self.eventlist if e.is_pending() ]
      if limit > 0:
         el = el[:limit]
      summary  = "\n".join ([e.longdesc() for e in el])
      return kramdown (summary)



def ical_replace (m):
   args   = m.group (2).split ()
   format = "summary"
   limit  = -1
   url    = default_url

   if len (args) >= 1:
      if ":" in args[0]:
         format, limit = args[0].split (":", 2)
         limit = int (limit)
      else:
         format = args[0]

   if len (args) >= 2:
      url = args[1]

   if not calendars.has_key (url):
      calendars[url] = Calendar(url)

   if format == "full":
      txtdata = calendars[url].get_fulllist (limit)
   else:
      txtdata = calendars[url].get_summary (limit)

   return m.group(1) + txtdata + m.group(3)



if __name__ == '__main__':
   if not sys.argv[1:]:
      print Calendar().get_fulllist()

   for f in sys.argv[1:]:
      data = open (f).read ()
      data2 = re.sub (r'(?ims)(<!--\s*ical\b\s*(.*?)\s*-->).*?(<!--\s*/ical\s*-->)',
                      ical_replace, data)

      if data2 != data:
         outf = open (f, "w")
         outf.write (data2)
         outf.close ()

