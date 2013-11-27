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
import uuid

default_url = "https://www.google.com/calendar/ical/bhj0m4hpsiqa8gpfdo8vb76p7k%40group.calendar.google.com/public/basic.ics"

calendars = {}

# figure out the day start in local time
now = datetime.datetime.now (dateutil.tz.tzlocal ())
now = now.replace (hour=0, minute=0, second=0, microsecond=0)
now = now.astimezone (dateutil.tz.tzutc ())


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
   def __init__ (self, entries):
      for k, v in entries.items ():
         self[k] = v
      self.upd = None


   def set_update_events (self, updates):
      if len (updates) > 0:
         self.upd = updates[0]
         self.upd.set_update_events (updates[1:])


   def shortdesc (self):
      r = []
      tim, evt = self.get_time()[0]

      if evt["SUMMARY"]:
         r.append ("* %s: <a name=\"summary-%s\" href=\"/calendar/#item-%s\">%s</a>" % (str (tim.strftime ("__%d. %m. %Y__")),
                                                                                        evt["UID"], evt["UID"], evt["SUMMARY"]))

      return "\n\n".join (r) + "\n"


   def longdesc (self):
      r = []
      tim, evt = self.get_time()[0]
      if evt["SUMMARY"]:
         r.append ("## <a name=\"item-%s\" href=\"/calendar/#summary-%s\">%s</a>" % (evt["UID"], evt["UID"], evt["SUMMARY"]))

      r.append (str (tim.strftime ("__%d. %m. %Y, %H:%M Uhr__")) + "\n")
      if evt["DESCRIPTION"]:
         r.append (evt["DESCRIPTION"] + "\n")

      if evt["LOCATION"]:
         r.append ("_Ort:_ " + evt["LOCATION"])

      if evt["URL"]:
         r.append ("_weitere Infos:_ [%s](%s)" % (evt["URL"], evt["URL"]))

      pending = self.get_time()[1:]
      if pending:
         r.append ("_Folgetermine:_ " +
                   ", ".join ([p[0].strftime ("%d. %m. %Y")
                              for p in pending[:3]]) + [".", "…"][len (pending) > 3])
      return "\n\n".join (r) + "\n"


   def __getitem__(self, key):
      return super (Event, self).get (key, None)


   def __setitem__(self, key, value):
      rdict = { 'n' : "\n" }
      value = re.sub ("\\\\(.)",
                      lambda x: rdict.get (x.group(1), x.group(1)), value)
      super (Event, self).__setitem__ (key, value)


   def __lt__ (self, other):
      return self.get_time ()[0][0] < other.get_time ()[0][0]


   def is_pending (self):
      return now < self.get_time ()[0][0]


   def get_time (self, times = []):
      if self.has_key ("RECURRENCE-ID"):
         rec = dateutil.parser.parse (self["RECURRENCE-ID"],
                                      tzinfos = simple_tzinfos)
         times = [t for t in times if t[0] != rec]

      if self.has_key ("DTSTART") and self.has_key ("RRULE"):
         rr = dateutil.rrule.rrulestr (self.rrtext, tzinfos = simple_tzinfos)
         pending = rr.between (now, now + datetime.timedelta (120))
         times = times + [ (p.astimezone (dateutil.tz.tzlocal ()), self)
                           for p in pending ]

      elif self.has_key ("DTSTART"):
         dts = dateutil.parser.parse (self["DTSTART"], tzinfos = simple_tzinfos)
         times = times + [ (dts.astimezone (dateutil.tz.tzlocal ()), self) ]

      else:
         times = times + [ (now.astimezone (dateutil.tz.tzlocal ()), self) ]

      if self.upd:
         times = self.upd.get_time (times)

      times.sort ()
      while len (times) > 1 and times[0][0] < now:
         times = times[1:]
      return times



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

      self.eventdict = {}
      cur_event = None
      raw_rrtext = ""

      for l in lines:
         if not l:
            continue

         extra = None
         key, value = l.split (":", 1)

         if ";" in key:
            key, extra = key.split (";", 1)

         if key == "BEGIN" and value == "VEVENT":
            cur_event = {}
            raw_rrtext = ""
            continue

         if key in ["RRULE", "RRULE", "RDATE", "EXRULE", "EXDATE", "DTSTART"]:
            raw_rrtext = raw_rrtext + "%s:%s\n" % (key, value)

         if key == "END" and value == "VEVENT":
            if not cur_event.has_key ("UID"):
               cur_event["UID"] = "%s" % uuid.uuid1()
            uid = cur_event["UID"]
            if not self.eventdict.has_key (uid):
               self.eventdict[uid] = []
            self.eventdict[uid].append (Event (cur_event))
            self.eventdict[uid][-1].rrtext = raw_rrtext
            cur_event = None
            continue

         if cur_event != None:
            cur_event[key] = value

      self.eventlist = []

      for ev in self.eventdict.values ():
         ev.sort ( lambda x, y: int (x.get ("SEQUENCE", "0")) -
                                int (y.get ("SEQUENCE", "0")))
         ev[0].set_update_events (ev[1:])
         self.eventlist.append (ev[0])

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

