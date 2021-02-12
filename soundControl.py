import pulsectl
import wx
import wx.lib.newevent
from threading import Thread

EVT_RESULT_ID = wx.NewId()

def EVT_RESULT(win, func):
     win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
     def __init__(self, data):
         wx.PyEvent.__init__(self)
         self.SetEventType(EVT_RESULT_ID)
         self.data = data

class SoundControl(Thread):

    def __init__(self, wxWindow):
       Thread.__init__(self)
       self.wxWindow = wxWindow

    def run(self):
       self.listen_events()

    def listen_events(self):
       with pulsectl.Pulse('event-listener') as pulse:

           def event_handler(ev):
              #print('Pulse event:', ev)
              wx.PostEvent(self.wxWindow, ResultEvent(None))
              #print('Event sent', ev)


           #print('listening...')
           pulse.event_mask_set('source')
           pulse.event_callback_set(event_handler)
           pulse.event_listen(timeout=0)


def is_default_muted():
#         help(pulseMute)
     with pulsectl.Pulse('m5ute') as pulseMute:
         default_source=pulseMute.get_source_by_name(pulseMute.server_info().default_source_name)
         #print("Checking active mic for mute",default_source)
         if(default_source.mute):
            return True;
         else:
            return False;

def mute():
      with pulsectl.Pulse('m5ute') as pulseMute:
        active_sources = [s for s in pulseMute.source_list() if s.port_active]
        for m in active_sources:
          pulseMute.source_mute(m.index, 1)

def unmute():
      with pulsectl.Pulse('m5ute') as pulseMute:
        active_sources = [s for s in pulseMute.source_list() if s.port_active]
        for m in active_sources:
          pulseMute.source_mute(m.index, 0)

#      active_sources = [s for s in pulseMute.source_list() if s.port_active]
     # if not active_sources:
    #    print("There are no active microphones, so not muting anything")
      #else:
        #if len(active_sources) > 1:
          #print("There are {} active mics".format(len(active_sources)))
#      for m in active_sources:
        #print("Checking active mic for mute", m.description, m.mute)
#        if(not m.mute):
#          print("At least one is unmuted", m.description, m.mute)
#          return False
